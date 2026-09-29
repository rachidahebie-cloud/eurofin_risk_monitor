"""Baseline naïve : la volatilité future = la volatilité récente (5 jours)."""
import pandas as pd


def predict_baseline(features: pd.DataFrame) -> pd.Series:
    return features["vol_5d"]
