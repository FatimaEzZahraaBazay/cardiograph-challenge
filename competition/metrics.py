import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error


def calculate_rmse(y_true, y_pred):
    """Calculate RMSE for QT predictions."""
    y_pred_clipped = np.clip(y_pred, 300.0, 500.0)
    return float(np.sqrt(mean_squared_error(y_true, y_pred_clipped)))


def evaluate_submission(y_true, y_pred):
    """Evaluate with RMSE and MAE."""
    y_pred_clipped = np.clip(y_pred, 300.0, 500.0)
    rmse = calculate_rmse(y_true, y_pred)
    mae = float(mean_absolute_error(y_true, y_pred_clipped))
    
    return {
        'rmse': rmse,
        'mae': mae,
        'primary_metric': rmse
    }