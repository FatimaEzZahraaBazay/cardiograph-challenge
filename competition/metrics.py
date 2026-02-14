import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error


def calculate_rmse(y_true, y_pred):
    """Calculate RMSE for QT predictions."""
    y_pred_clipped = np.clip(y_pred, 300.0, 500.0)
    return float(np.sqrt(mean_squared_error(y_true, y_pred_clipped)))


def evaluate_submission(y_true, y_pred):
    """Evaluate with RMSE, MAE, and tolerance metric."""
    y_pred_clipped = np.clip(y_pred, 300.0, 500.0)
    rmse = calculate_rmse(y_true, y_pred)
    mae = float(mean_absolute_error(y_true, y_pred_clipped))
    
    # Calculate percentage of predictions within ±10ms of true value
    errors = np.abs(y_true - y_pred_clipped)
    within_10ms = np.sum(errors <= 10.0)
    within_tolerance_10ms = (within_10ms / len(y_true)) * 100.0

    return {
        'rmse': rmse,
        'mae': mae,
        'within_tolerance_10ms': float(within_tolerance_10ms),
        'primary_metric': rmse
    }