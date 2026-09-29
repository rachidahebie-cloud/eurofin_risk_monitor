# EuroFin Risk Monitor

Pipeline automatisé et prévision de volatilité des banques et assurances européennes
(BNP Paribas, Crédit Agricole, Société Générale, AXA, Allianz).

**Dashboard en ligne :** _lien Streamlit Cloud à ajouter_

## Objectif
Suivre chaque jour le risque de marché des grandes banques et assurances, le relier à la politique
monétaire de la BCE, et prévoir la volatilité à 5 jours.

## Architecture
```
yfinance + API BCE  ->  nettoyage (Pandas)  ->  SQLite  ->  indicateurs + prévisions  ->  Streamlit
        ^                                                          ^
        └────────── GitHub Actions (quotidien / réentraînement hebdo) ┘
```

## Données
- Cours de Bourse : yfinance (5 valeurs + CAC 40 en référence)
- Taux directeur BCE : API SDMX de la BCE

## Modèles de volatilité
Baseline naïve, GARCH(1,1) et Random Forest, comparés en validation walk-forward
(RMSE, MAE, QLIKE). _Résultats à compléter dans `reports/conclusions.md`._

## Structure
```
eurofin-risk-monitor/
├── .github/workflows/   # daily_pipeline.yml, weekly_retrain.yml
├── data/                # eurofin.db (SQLite, mis à jour par le pipeline)
├── models/              # modèle entraîné
├── notebooks/           # exploration, comparaison de modèles
├── reports/             # figures, métriques, conclusions
├── sql/                 # schema.sql, queries.sql
├── src/                 # extract / transform / load / models / pipeline
├── dashboard/app.py     # application Streamlit
└── tests/
```

## Installation et exécution
```bash
git clone https://github.com/<ton-pseudo>/eurofin-risk-monitor.git
cd eurofin-risk-monitor
python -m venv .venv && .venv\Scripts\activate    # Windows
pip install -r requirements.txt

python -m src.pipeline          # extraction + indicateurs + prédictions
python -m src.models.train      # entraînement du modèle
streamlit run dashboard/app.py
pytest
```

## Auteur
TIE RACHIDA HEBIE — Étudiante en BUT Informatique
