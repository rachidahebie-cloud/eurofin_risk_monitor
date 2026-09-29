"""Configuration centrale du projet."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "eurofin.db"
MODEL_PATH = ROOT / "models" / "rf_vol.joblib"
METRICS_PATH = ROOT / "reports" / "metrics.json"

# ticker Yahoo Finance -> (nom, secteur)
TICKERS = {
    "BNP.PA": ("BNP Paribas", "Banque"),
    "ACA.PA": ("Crédit Agricole", "Banque"),
    "GLE.PA": ("Société Générale", "Banque"),
    "CS.PA": ("AXA", "Assurance"),
    "ALV.DE": ("Allianz", "Assurance"),
}
BENCHMARK = "^FCHI"  # CAC 40

START_DATE = "2015-01-01"
TRADING_DAYS = 252
VOL_HORIZON = 5  # on prédit la volatilité réalisée sur les 5 prochains jours

# Taux de la facilité de dépôt BCE (API SDMX)
ECB_URL = "https://data-api.ecb.europa.eu/service/data/FM/B.U2.EUR.4F.KR.DFR.LEV"
