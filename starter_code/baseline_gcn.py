"""
CardioGraph Baseline: GCN for QT Regression
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv, global_mean_pool
from torch_geometric.loader import DataLoader
import numpy as np
import pandas as pd
import os

torch.manual_seed(42)

class GCN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = GCNConv(3, 64)
        self.conv2 = GCNConv(64, 64)
        self.regressor = nn.Linear(64, 1)
    
    def forward(self, data):
        x, edge_index, batch = data.x, data.edge_index, data.batch
        x = F.relu(self.conv1(x, edge_index))
        x = F.dropout(x, p=0.5, training=self.training)
        x = F.relu(self.conv2(x, edge_index))
        x = global_mean_pool(x, batch)
        return self.regressor(x)

print("🫀 CardioGraph Baseline\n")

# Load (with weights_only=False for PyTorch 2.10+)
train_graphs = torch.load('../data/public/train_graphs.pt', weights_only=False)
val_size = int(0.2 * len(train_graphs))
train_data, val_data = train_graphs[:-val_size], train_graphs[-val_size:]

train_loader = DataLoader(train_data, batch_size=4, shuffle=True)
val_loader = DataLoader(val_data, batch_size=4)

# Train
model = GCN()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

for epoch in range(100):
    model.train()
    for batch in train_loader:
        optimizer.zero_grad()
        loss = F.mse_loss(model(batch).squeeze(), batch.y)
        loss.backward()
        optimizer.step()
    
    if (epoch+1) % 20 == 0:
        model.eval()
        preds, true = [], []
        with torch.no_grad():
            for batch in val_loader:
                pred = model(batch).squeeze()
                if pred.dim() == 0:
                    preds.append(pred.item())
                else:
                    preds.extend(pred.tolist())
                true.extend(batch.y.tolist())
        rmse = np.sqrt(np.mean((np.array(true) - np.array(preds))**2))
        print(f"Epoch {epoch+1}: RMSE = {rmse:.2f} ms")

# Predict test (with weights_only=False for PyTorch 2.10+)
test_graphs = torch.load('../data/public/test_graphs.pt', weights_only=False)
test_loader = DataLoader(test_graphs, batch_size=4)

preds = []
model.eval()
with torch.no_grad():
    for batch in test_loader:
        pred = model(batch).squeeze()
        if pred.dim() == 0:
            preds.append(pred.item())
        else:
            preds.extend(pred.tolist())

# Save
os.makedirs('../submissions/inbox/baseline/run_001', exist_ok=True)
pd.DataFrame({'id': range(len(preds)), 'y_pred': preds}).to_csv(
    '../submissions/inbox/baseline/run_001/predictions.csv', index=False)

import json
with open('../submissions/inbox/baseline/run_001/metadata.json', 'w') as f:
    json.dump({"team": "baseline", "run_id": "run_001", "author_type": "human",
               "model": "GCN-2layers", "notes": "Simple baseline"}, f, indent=2)

print("\n✅ Saved to: submissions/inbox/baseline/run_001/")