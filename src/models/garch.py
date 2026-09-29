"""GARCH(1,1) via la librairie arch."""
import numpy as np
import pandas as pd
from arch import arch_model

from src.config import TRADING_DAYS, VOL_HORIZON


def forecast_garch(returns: pd.Series, horizon: int = VOL_HORIZON) -> float:
    """Volatilité annualisée moyenne prévue sur `horizon` jours."""
    r = returns.dropna() * 100  # arch fonctionne mieux avec des rendements en %
    res = arch_model(r, vol="GARCH", p=1, q=1, mean="Constant", dist="normal").fit(disp="off")
    var = res.forecast(horizon=horizon).variance.iloc[-1].values
    return float(np.sqrt(var.mean()) / 100 * np.sqrt(TRADING_DAYS))

# TODO (notebook 02) : évaluation walk-forward du GARCH (refit tous les N jours)
