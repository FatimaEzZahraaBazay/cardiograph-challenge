import pandas as pd
import sys
from metrics import evaluate_submission

def main(pred_path, label_path):
    preds = pd.read_csv(pred_path).sort_values("id")
    labels = pd.read_csv(label_path).sort_values("id")

    merged = labels.merge(preds, on="id", how="inner")
    if len(merged) != len(labels):
        raise ValueError("ID mismatch")

    y_true = merged["qt_interval"].values
    y_pred = merged["y_pred"].values
    
    results = evaluate_submission(y_true, y_pred)
    
    print(f"SCORE={results['primary_metric']:.8f}")
    print(f"RMSE={results['rmse']:.8f}")
    print(f"MAE={results['mae']:.8f}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])