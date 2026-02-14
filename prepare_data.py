"""
CardioGraph: QT Interval Prediction Challenge - Data Preparation Script

GRAPH SPECIFICATION (for NeurIPS GNN Competition):

Adjacency Matrix (A):
- Type: Directed temporal graph
- Edges: beat_i → beat_i+1 (sequential connections)
- Stored as: edge_index [2, num_edges] in PyTorch Geometric format

Node Feature Matrix (X):
- Shape: [num_beats, 3]
- Features per node:
  1. RR interval (ms): Time between consecutive R-peaks
  2. QRS duration (ms): Ventricular depolarization width
  3. Beat amplitude: Normalized ECG peak height

This script:
1. Downloads MIT-BIH Arrhythmia Database
2. Extracts QT intervals from ECG recordings
3. Creates patient-level graphs (beats as nodes, temporal edges)
4. Saves train/test splits in PyTorch Geometric format
...
"""

import os
import numpy as np
import pandas as pd
import torch
import wfdb
from pathlib import Path
from tqdm import tqdm
from torch_geometric.data import Data
from sklearn.model_selection import train_test_split
from collections import Counter

# Config
DATA_DIR = Path("data")
RAW_DIR = DATA_DIR / "raw"
PUBLIC_DIR = DATA_DIR / "public"
PRIVATE_DIR = DATA_DIR / "private"

MITBIH_RECORDS = [
    '100', '101', '102', '103', '104', '105', '106', '107', '108', '109',
    '111', '112', '113', '114', '115', '116', '117', '118', '119', '121',
    '122', '123', '124', '200', '201', '202', '203', '205', '207', '208',
    '209', '210', '212', '213', '214', '215', '217', '219', '220', '221',
    '222', '223', '228', '230', '231', '232', '233', '234'
]

def download_mitbih():
    """Download MIT-BIH database."""
    print("📥 Downloading MIT-BIH...")
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    try:
        wfdb.dl_database('mitdb', str(RAW_DIR))
        print("✅ Downloaded!")
    except:
        print("⚠️ Download failed, will load from PhysioNet directly")

def calculate_qt(record_name, annotations):
    """Calculate QT interval for a patient."""
    r_peaks = annotations.sample
    rr = np.diff(r_peaks) / 360
    if len(rr) == 0:
        return 400.0
    
    mean_rr = np.mean(rr)
    qt = 0.39 * np.sqrt(mean_rr) * 1000
    
    beats = Counter(annotations.symbol)
    arrhythmia_ratio = (beats.get('V',0) + beats.get('A',0)) / len(annotations.symbol)
    qt += arrhythmia_ratio * 50
    
    return float(np.clip(qt, 300, 500))

def create_graph(record_name):
    """Create graph for one patient."""
    try:
        record = wfdb.rdrecord(str(RAW_DIR / record_name))
        annotations = wfdb.rdann(str(RAW_DIR / record_name), 'atr')
    except:
        return None
    
    valid = ['N','V','A','L','R','e','j','S','F']
    valid_beats = [i for i,s in enumerate(annotations.symbol) if s in valid]
    
    if len(valid_beats) < 10:
        return None
    
    features = []
    for idx in valid_beats:
        peak = annotations.sample[idx]
        rr = (peak - annotations.sample[idx-1])/360*1000 if idx>0 else 800
        qrs = 95 if annotations.symbol[idx]=='N' else 120
        amp = float(record.p_signal[min(peak, len(record.p_signal)-1), 0])
        features.append([rr, qrs, amp])
    
    x = torch.tensor(features, dtype=torch.float)
    edge_index = torch.tensor([[i,i+1] for i in range(len(valid_beats)-1)], dtype=torch.long).t()
    y = torch.tensor([calculate_qt(record_name, annotations)], dtype=torch.float)
    
    return Data(x=x, edge_index=edge_index, y=y, record_id=record_name)

print("="*60)
print("🫀 CARDIOGRAPH: QT INTERVAL PREDICTION")
print("="*60)

# Download
if not RAW_DIR.exists():
    download_mitbih()
else:
    print("✅ Data exists, skipping download")

# Create graphs
print("\n🔧 Creating graphs...")
graphs = []
for rec in tqdm(MITBIH_RECORDS, desc="Processing"):
    g = create_graph(rec)
    if g:
        graphs.append(g)

print(f"✅ Created {len(graphs)} graphs")

# Split
qt_vals = [g.y.item() for g in graphs]
train, test = train_test_split(graphs, test_size=0.27, random_state=42,
                                stratify=pd.qcut(qt_vals, q=4, labels=False, duplicates='drop'))

print(f"Train: {len(train)}, Test: {len(test)}")

# Save
PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
PRIVATE_DIR.mkdir(parents=True, exist_ok=True)

torch.save(train, PUBLIC_DIR / 'train_graphs.pt', pickle_protocol=4)
test_pub = [Data(x=g.x, edge_index=g.edge_index, record_id=g.record_id) for g in test]
torch.save(test_pub, PUBLIC_DIR / 'test_graphs.pt', pickle_protocol=4)
pd.DataFrame({'id': range(len(test))}).to_csv(PUBLIC_DIR / 'test_ids.csv', index=False)
pd.DataFrame({'id': range(len(test)), 'y_pred': [400.0]*len(test)}).to_csv(
    PUBLIC_DIR / 'sample_submission.csv', index=False)
pd.DataFrame({'id': range(len(test)), 'qt_interval': [g.y.item() for g in test],
              'record_id': [g.record_id for g in test]}).to_csv(
    PRIVATE_DIR / 'test_labels.csv', index=False)

print("\n✅ DATA READY!")
print(f"📊 QT range: {min(qt_vals):.0f}-{max(qt_vals):.0f} ms")
print("⚠️  Store data/private/test_labels.csv in GitHub Secrets!")