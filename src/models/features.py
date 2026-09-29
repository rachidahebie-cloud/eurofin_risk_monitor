"""Construction des variables. Toutes calculées avec l'information disponible à la date t
(pas de fuite de données) ; seule la cible regarde le futur."""
import numpy as np
import pandas as pd

from src.config import BENCHMARK, TRADING_DAYS, VOL_HORIZON

FEATURES = ["vol_5d", "vol_10d", "vol_30d", "ret_1d", "ret_5d",
            "volume_chg", "bench_vol_10d", "ecb_rate"]


def build_features(prices: pd.DataFrame, rates: pd.DataFrame, ticker: str) -> pd.DataFrame:
    ann = np.sqrt(TRADING_DAYS)
    p = prices[prices["ticker"] == ticker].set_index("date").sort_index()
    b = prices[prices["ticker"] == BENCHMARK].set_index("date").sort_index()
    ret = np.log(p["close"]).diff()
    bench_ret = np.log(b["close"]).diff().reindex(p.index)

    df = pd.DataFrame(index=p.index)
    for w in (5, 10, 30):
        df[f"vol_{w}d"] = ret.rolling(w).std() * ann
    df["ret_1d"] = ret
    df["ret_5d"] = ret.rolling(5).sum()
    df["volume_chg"] = np.log(p["volume"].replace(0, np.nan)).diff()
    df["bench_vol_10d"] = bench_ret.rolling(10).std() * ann
    rate = rates.set_index("date")["rate"].sort_index()
    df["ecb_rate"] = rate.reindex(df.index, method="ffill")
    # Cible : vol réalisée sur t+1..t+H
    df["target"] = ret.rolling(VOL_HORIZON).std().shift(-VOL_HORIZON) * ann
    df["ticker"] = ticker
    return df
