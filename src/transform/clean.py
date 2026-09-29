"""Nettoyage des données brutes."""
import pandas as pd


def clean_prices(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates(subset=["ticker", "date"]).sort_values(["ticker", "date"])
    df = df.dropna(subset=["close"])
    df = df[df["close"] > 0]
    return df.reset_index(drop=True)
