"""Dashboard Streamlit :  streamlit run dashboard/app.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd
import plotly.express as px
import streamlit as st

from src.config import DB_PATH, TICKERS
from src.load.database import read_sql

st.set_page_config(page_title="EuroFin Risk Monitor", page_icon="📊", layout="wide")
st.title("📊 EuroFin Risk Monitor")
st.caption("Banques & assurances européennes : indicateurs de risque et prévision de volatilité")

if not DB_PATH.exists():
    st.error("Base de données introuvable : lance d'abord `python -m src.pipeline`.")
    st.stop()

names = {t: f"{n} ({t})" for t, (n, _) in TICKERS.items()}
ticker = st.sidebar.selectbox("Valeur", list(TICKERS), format_func=names.get)

prices = read_sql("SELECT date, close FROM prices WHERE ticker = ? ORDER BY date", (ticker,))
ind = read_sql("SELECT * FROM indicators WHERE ticker = ? ORDER BY date", (ticker,))
pred = read_sql("SELECT * FROM vol_predictions WHERE ticker = ? ORDER BY date", (ticker,))
ecb = read_sql("SELECT * FROM ecb_rates ORDER BY date")

if ind.empty:
    st.warning("Pas encore d'indicateurs.")
    st.stop()

last = ind.iloc[-1]
c1, c2, c3, c4 = st.columns(4)
c1.metric("Dernière date", last["date"])
c2.metric("Volatilité 30j", f"{last['vol_30d']:.1%}")
c3.metric("Drawdown", f"{last['drawdown']:.1%}")
c4.metric("Bêta 90j vs CAC 40", f"{last['beta_90d']:.2f}")

tab1, tab2, tab3 = st.tabs(["Cours", "Volatilité", "Taux BCE"])
with tab1:
    st.plotly_chart(px.line(prices, x="date", y="close", title="Cours de clôture"),
                    use_container_width=True)
with tab2:
    fig = px.line(ind, x="date", y=["vol_30d", "vol_90d"], title="Volatilité annualisée observée")
    st.plotly_chart(fig, use_container_width=True)
    st.subheader("Prévisions de volatilité à 5 jours")
    if pred.empty:
        st.info("Aucune prévision stockée pour le moment.")
    else:
        st.dataframe(pred.tail(15), use_container_width=True)
        # TODO : alerte si la vol prévue dépasse un seuil ; courbe observé vs prédit
with tab3:
    st.plotly_chart(px.line(ecb, x="date", y="rate", title="Taux facilité de dépôt BCE (%)"),
                    use_container_width=True)
