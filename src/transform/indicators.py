"""Indicateurs financiers : rendement, volatilité, drawdown, bêta."""
import numpy as np
import pandas as pd

from src.config import BENCHMARK, TRADING_DAYS


def compute_indicators(prices: pd.DataFrame, benchmark: str = BENCHMARK) -> pd.DataFrame:
    close = prices.pivot(index="date", columns="ticker", values="close").sort_index()
    ret = np.log(close).diff()
    bench = ret[benchmark]
    frames = []
    for t in [c for c in close.columns if c != benchmark]:
        r = ret[t]
        df = pd.DataFrame({"ret": r})
        df["vol_30d"] = r.rolling(30).std() * np.sqrt(TRADING_DAYS)
        df["vol_90d"] = r.rolling(90).std() * np.sqrt(TRADING_DAYS)
        df["drawdown"] = close[t] / close[t].cummax() - 1
        df["beta_90d"] = r.rolling(90).cov(bench) / bench.rolling(90).var()
        df["ticker"] = t
        frames.append(df.rename_axis("date").reset_index())
    cols = ["ticker", "date", "ret", "vol_30d", "vol_90d", "drawdown", "beta_90d"]
    return pd.concat(frames, ignore_index=True)[cols]
