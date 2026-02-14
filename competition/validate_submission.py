"""
Validate submission format for CardioGraph.
"""

import pandas as pd
import sys


def main(pred_path, test_ids_path):
    """
    Validate predictions.csv format.
    
    Args:
        pred_path: Path to predictions.csv
        test_ids_path: Path to test_ids.csv
    """
    preds = pd.read_csv(pred_path)
    test_ids = pd.read_csv(test_ids_path)
    
    # Check columns
    if "id" not in preds.columns or "y_pred" not in preds.columns:
        raise ValueError("predictions.csv must contain 'id' and 'y_pred' columns")
    
    # Check for duplicates
    if preds["id"].duplicated().any():
        raise ValueError("Duplicate IDs found in predictions")
    
    # Check for NaN
    if preds["y_pred"].isna().any():
        raise ValueError("NaN predictions found")
    
    # Check valid range [300, 500] ms
    if ((preds["y_pred"] < 300) | (preds["y_pred"] > 500)).any():
        raise ValueError("Predictions must be in range [300, 500] ms")
    
    # Check ID matching
    if set(preds["id"]) != set(test_ids["id"]):
        raise ValueError("Prediction IDs do not match test_ids.csv")
    
    # Check count
    if len(preds) != len(test_ids):
        raise ValueError(f"Wrong number of predictions: {len(preds)} vs {len(test_ids)} expected")
    
    print("VALID SUBMISSION")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python validate_submission.py <predictions.csv> <test_ids.csv>")
        sys.exit(1)
    
    main(sys.argv[1], sys.argv[2])