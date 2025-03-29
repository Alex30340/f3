import streamlit as st
import yfinance as yf
import pandas as pd
import altair as alt

def run():
    st.set_page_config(page_title="Analyse Technique", layout="wide")
    st.title("📊 Analyse Technique Universelle")
    st.markdown("✅ **Sélectionne un actif** *(actions, crypto, forex...)*")

    actifs = {
        "Bitcoin (Crypto)": "BTC-USD",
        "Ethereum (Crypto)": "ETH-USD",
        "EUR/USD (Forex)": "EURUSD=X",
        "USD/JPY (Forex)": "JPY=X",
        "Tesla (Action)": "TSLA"
    }

    choix = st.selectbox("Choisis un actif", list(actifs.keys()))
    symbole = actifs[choix]

    if st.button("Analyser"):
        try:
            data = yf.download(symbole, period="3mo", interval="1d")
            data = data.dropna()

            if data.empty:
                st.warning("Aucune donnée récupérée pour cet actif.")
                return

            data.reset_index(inplace=True)

            # 🛠️ S'assurer que les données sont bien plates (1D)
            data['Close'] = data['Close'].astype(float)

            # 📈 Graphique type TradingView simple (bougie possible après)
            chart = alt.Chart(data).mark_line().encode(
                x=alt.X('Date:T', title='Date'),
                y=alt.Y('Close:Q', title='Prix de clôture')
            ).properties(
                title=f"Données de {choix}",
                width='container'
            )

            st.altair_chart(chart, use_container_width=True)

        except Exception as e:
            st.error(f"Erreur lors de l'analyse : {e}")
