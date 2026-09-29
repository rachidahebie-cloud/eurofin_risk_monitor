"""Extraction des cours de Bourse via yfinance."""
import logging

import pandas as pd
import yfinance as yf

from src.config import BENCHMARK, START_DATE, TICKERS

logger = logging.getLogger(__name__)


def fetch_prices(start: str | None = None, tickers: list[str] | None = None) -> pd.DataFrame:
    """Retourne un DataFrame long : ticker, date, open, high, low, close, volume."""
    tickers = tickers or [*TICKERS, BENCHMARK]
    frames = []
    for t in tickers:
        hist = yf.Ticker(t).history(start=start or START_DATE, auto_adjust=True)
        if hist.empty:
            logger.warning("Aucune donnée pour %s", t)
            continue
        hist = hist.reset_index().rename(columns=str.lower)
        hist["date"] = pd.to_datetime(hist["date"]).dt.tz_localize(None).dt.normalize()
        hist["ticker"] = t
        frames.append(hist[["ticker", "date", "open", "high", "low", "close", "volume"]])
    if not frames:
        raise RuntimeError("Aucune donnée récupérée depuis yfinance")
    return pd.concat(frames, ignore_index=True)
