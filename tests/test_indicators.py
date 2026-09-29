import numpy as np
import pandas as pd

from src.models.evaluate import qlike
from src.transform.indicators import compute_indicators


def _fake_prices(n=200):
    rng = np.random.default_rng(0)
    dates = pd.bdate_range("2023-01-02", periods=n)
    frames = []
    for t in ["AAA", "^FCHI"]:
        close = 100 * np.exp(np.cumsum(rng.normal(0, 0.01, n)))
        frames.append(pd.DataFrame({"ticker": t, "date": dates, "close": close}))
    return pd.concat(frames, ignore_index=True)


def test_indicators_shape_and_ranges():
    out = compute_indicators(_fake_prices())
    assert set(out["ticker"]) == {"AAA"}  # le benchmark n'est pas une ligne de sortie
    assert (out["drawdown"] <= 0).all()
    assert (out["vol_30d"].dropna() > 0).all()


def test_qlike_zero_when_perfect():
    assert qlike([0.2, 0.3], [0.2, 0.3]) == 0.0
