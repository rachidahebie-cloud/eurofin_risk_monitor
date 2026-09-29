"""Métriques d'évaluation des prévisions de volatilité."""
import numpy as np


def rmse(y_true, y_pred) -> float:
    return float(np.sqrt(np.mean((np.asarray(y_true) - np.asarray(y_pred)) ** 2)))


def mae(y_true, y_pred) -> float:
    return float(np.mean(np.abs(np.asarray(y_true) - np.asarray(y_pred))))


def qlike(y_true, y_pred, eps: float = 1e-8) -> float:
    """QLIKE sur les variances (métrique standard pour la volatilité)."""
    s_t = np.maximum(np.asarray(y_true) ** 2, eps)
    s_p = np.maximum(np.asarray(y_pred) ** 2, eps)
    return float(np.mean(s_t / s_p - np.log(s_t / s_p) - 1))


def all_metrics(y_true, y_pred) -> dict:
    return {"rmse": rmse(y_true, y_pred), "mae": mae(y_true, y_pred), "qlike": qlike(y_true, y_pred)}
