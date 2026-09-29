"""Extraction du taux directeur BCE (facilité de dépôt) via l'API SDMX."""
import io

import pandas as pd
import requests

from src.config import ECB_URL


def fetch_ecb_rate(start: str | None = None) -> pd.DataFrame:
    """Retourne un DataFrame : date, rate (en %)."""
    params = {"format": "csvdata"}
    if start:
        params["startPeriod"] = start
    resp = requests.get(ECB_URL, params=params, timeout=30)
    resp.raise_for_status()
    df = pd.read_csv(io.StringIO(resp.text))
    out = df[["TIME_PERIOD", "OBS_VALUE"]].rename(
        columns={"TIME_PERIOD": "date", "OBS_VALUE": "rate"}
    )
    out["date"] = pd.to_datetime(out["date"])
    return out.dropna().sort_values("date").reset_index(drop=True)
