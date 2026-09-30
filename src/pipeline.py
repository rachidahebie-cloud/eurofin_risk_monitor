"""Pipeline quotidien : extraction -> nettoyage -> stockage -> indicateurs -> prédictions.
Lancé par GitHub Actions :  python -m src.pipeline"""
import logging

import joblib
import numpy as np
import pandas as pd

from src.config import MODEL_PATH, START_DATE, TICKERS, VOL_HORIZON
from src.extract.ecb import fetch_ecb_rate
from src.extract.prices import fetch_prices
from src.load.database import init_db, read_sql, upsert
from src.models.baseline import predict_baseline
from src.models.features import FEATURES, build_features
from src.transform.clean import clean_prices
from src.transform.indicators import compute_indicators

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)


def _start_date() -> str:
    last = read_sql("SELECT MAX(date) AS d FROM prices")["d"].iloc[0]
    if last is None:
        return START_DATE
    return (pd.Timestamp(last) - pd.Timedelta(days=10)).strftime("%Y-%m-%d")


def predict_and_store(prices: pd.DataFrame, rates: pd.DataFrame) -> None:
    model = joblib.load(MODEL_PATH) if MODEL_PATH.exists() else None
    if model is None:
        log.warning("Pas de modèle entraîné : seule la baseline est produite")
    out = []
    for t in TICKERS:
        feats = build_features(prices, rates, t).dropna(subset=FEATURES)
        if feats.empty:
            continue
        last = feats.iloc[[-1]]
        date = last.index[0]
        out.append((t, date, "baseline", float(predict_baseline(last).iloc[0])))
        if model is not None:
            out.append((t, date, "random_forest", float(model.predict(last[FEATURES])[0])))
        try:
            from src.models.garch import forecast_garch
            ret = np.log(prices[prices["ticker"] == t].set_index("date")["close"]).diff()
            out.append((t, date, "garch", forecast_garch(ret)))
        except Exception as exc:  # GARCH ne doit jamais casser le pipeline
            log.warning("GARCH ignoré pour %s : %s", t, exc)
    df = pd.DataFrame(out, columns=["ticker", "date", "model", "predicted_vol"])
    df["horizon"] = VOL_HORIZON
    upsert("vol_predictions", df[["ticker", "date", "horizon", "model", "predicted_vol"]])
    log.info("%d prédictions stockées", len(df))


def run() -> None:
    init_db()
    start = _start_date()
    log.info("Extraction depuis %s", start)
    prices = clean_prices(fetch_prices(start))
    upsert("prices", prices)
    upsert("ecb_rates", fetch_ecb_rate())  # série complète : quelques lignes seulement
    full = read_sql("SELECT * FROM prices")
    full["date"] = pd.to_datetime(full["date"])
    rates = read_sql("SELECT * FROM ecb_rates")
    rates["date"] = pd.to_datetime(rates["date"])

    upsert("indicators", compute_indicators(full))
    predict_and_store(full, rates)
    log.info("Pipeline terminé")


if __name__ == "__main__":
    run()
