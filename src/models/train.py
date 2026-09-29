"""Entraînement + comparaison walk-forward : baseline vs Random Forest.
Lancé chaque semaine par GitHub Actions :  python -m src.models.train"""
import json
import logging

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import TimeSeriesSplit

from src.config import METRICS_PATH, MODEL_PATH, TICKERS, VOL_HORIZON
from src.load.database import read_sql
from src.models.baseline import predict_baseline
from src.models.evaluate import all_metrics
from src.models.features import FEATURES, build_features

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def load_dataset() -> pd.DataFrame:
    prices = read_sql("SELECT * FROM prices")
    prices["date"] = pd.to_datetime(prices["date"])
    rates = read_sql("SELECT * FROM ecb_rates")
    rates["date"] = pd.to_datetime(rates["date"])
    frames = [build_features(prices, rates, t) for t in TICKERS]
    return pd.concat(frames).dropna(subset=FEATURES + ["target"]).sort_index()


def make_model() -> RandomForestRegressor:
    return RandomForestRegressor(n_estimators=200, max_depth=8, min_samples_leaf=20,
                                 n_jobs=-1, random_state=42)


def main() -> None:
    data = load_dataset()
    X, y = data[FEATURES], data["target"]
    # gap = chevauchement de la cible (H jours) pour éviter toute fuite entre train et test
    tscv = TimeSeriesSplit(n_splits=5, gap=VOL_HORIZON * len(TICKERS))
    rows = []
    for fold, (tr, te) in enumerate(tscv.split(X), 1):
        model = make_model().fit(X.iloc[tr], y.iloc[tr])
        rows.append({"fold": fold, "model": "baseline",
                     **all_metrics(y.iloc[te], predict_baseline(X.iloc[te]))})
        rows.append({"fold": fold, "model": "random_forest",
                     **all_metrics(y.iloc[te], model.predict(X.iloc[te]))})
    summary = pd.DataFrame(rows).groupby("model")[["rmse", "mae", "qlike"]].mean()
    log.info("\n%s", summary)

    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    METRICS_PATH.write_text(json.dumps(summary.to_dict("index"), indent=2))
    joblib.dump(make_model().fit(X, y), MODEL_PATH)
    log.info("Modèle sauvegardé : %s", MODEL_PATH)


if __name__ == "__main__":
    main()
