# CardioGraph: QT Interval Prediction Challenge

🫀 **Graph-level regression challenge for QT interval prediction from ECG signals**

---

## 📋 Overview

**CardioGraph** evaluates GNN models on predicting QT intervals from patient ECG graphs.

- **Task:** Graph Regression
- **Dataset:** MIT-BIH Arrhythmia Database (48 patients)
- **Metric:** RMSE (Root Mean Squared Error)
- **Baseline:** Simple 2-layer GCN → RMSE ~19-25 ms

---

## 🫀 What is QT Interval?

The **QT interval** measures the time from ventricular depolarization (Q wave) to repolarization (T wave).

- **Normal:** 350-450 ms
- **Prolonged (>450 ms):** Risk of sudden cardiac death ⚠️
- **Clinical use:** Drug safety testing, arrhythmia risk assessment

---

## 📊 Dataset

**Source:** MIT-BIH Arrhythmia Database (PhysioNet)

**Structure:**
- **48 patient graphs** (1 graph per patient)
- **Train:** 35 graphs (with QT labels)
- **Test:** 13 graphs (labels hidden)

**Each graph:**
- **Nodes:** Heartbeats (~2000 per patient)
- **Features:** [RR-interval, QRS duration, amplitude]
- **Edges:** Temporal (beat_i → beat_i+1)
- **Label:** QT interval in milliseconds (300-500 ms)

---

## 🎯 Submission Format

Submit `predictions.csv`:

```csv
id,y_pred
0,412.5
1,385.2
...
12,398.3
```

**Requirements:**
- `id`: 0 to 12 (must match test_ids.csv)
- `y_pred`: QT interval in ms [300, 500]

---

## 📤 How to Submit

1. Fork this repository
2. Create folder: `submissions/inbox/<team>/<run>/`
3. Add:
   - `predictions.csv`
   - `metadata.json`

**Example metadata.json:**
```json
{
  "team": "your_team",
  "run_id": "run_001",
  "author_type": "human",
  "model": "GAT-3layers",
  "notes": "Used attention on temporal edges"
}
```

4. Open Pull Request → Auto-scored!

---

## 🏆 Leaderboard

- **Markdown:** [leaderboard/leaderboard.md](leaderboard/leaderboard.md)
- **Interactive:** Enable GitHub Pages for filterable view

**Lower RMSE is better!**

---

## 📏 Evaluation

**Primary Metric:** RMSE

```
RMSE = sqrt(mean((y_true - y_pred)²))
```

**Lower is better!**
- Baseline: ~20-25 ms
- Good: <15 ms
- Excellent: <10 ms

---

## 🚀 Getting Started

See `starter_code/baseline_gcn.py` for a working 2-layer GCN example.

---

## 📜 Rules

**Allowed ✅**
- Any GNN architecture
- Offline training (<3h CPU)
- Feature engineering

**Not Allowed ❌**
- External datasets
- Test label access
- Modifying evaluation scripts

---

## 📞 Support

Open a GitHub issue for questions.

---

## 🎓 Citation

```bibtex
@misc{cardiograph2026,
  title={CardioGraph: QT Interval Prediction Challenge},
  author={Bazay, Fatima Ez-Zahraa},
  year={2026},
  publisher={GitHub}
}
```

---

**Good luck!** 🚀