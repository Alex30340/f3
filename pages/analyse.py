import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from ta.trend import MACD

st.set_page_config(page_title="Analyse Technique", layout="wide")

def run():
    st.title("📊 Analyse Technique Universelle")
    st.markdown("✅ **Sélectionne un actif** *(actions, crypto, forex...)*")

    actifs = {
        "Bitcoin (Crypto)": "BTC-USD",
        "Ethereum (Crypto)": "ETH-USD",
        "EUR/USD (Forex)": "EURUSD=X",
        "USD/JPY (Forex)": "JPY=X",
        "Tesla (Action)": "TSLA",
        "Apple (Action)": "AAPL"
    }

    actif_nom = st.selectbox("Choisis un actif", list(actifs.keys()))
    symbole = actifs[actif_nom]

    if st.button("Analyser"):
        try:
            df = yf.download(symbole, period="3mo", interval="1d")
            df.dropna(inplace=True)

            # ➤ MACD
            macd = MACD(close=df["Close"])
            df["MACD"] = macd.macd()
            df["Signal"] = macd.macd_signal()
            df["Histogramme"] = macd.macd_diff()

            # ➤ Graphique Bougies
            fig = go.Figure(data=[
                go.Candlestick(
                    x=df.index,
                    open=df["Open"],
                    high=df["High"],
                    low=df["Low"],
                    close=df["Close"],
                    name="Bougies"
                )
            ])

            fig.update_layout(title=f"Données de {actif_nom}", xaxis_title="Date", yaxis_title="Prix", height=600)
            st.plotly_chart(fig, use_container_width=True)

            # ➤ Graphique MACD
            fig_macd = go.Figure()
            fig_macd.add_trace(go.Scatter(x=df.index, y=df["MACD"], mode="lines", name="MACD"))
            fig_macd.add_trace(go.Scatter(x=df.index, y=df["Signal"], mode="lines", name="Signal"))
            fig_macd.add_trace(go.Bar(x=df.index, y=df["Histogramme"], name="Histogramme MACD"))

            fig_macd.update_layout(title="MACD", height=300)
            st.plotly_chart(fig_macd, use_container_width=True)

        except Exception as e:
            st.error(f"Erreur lors de l'analyse : {str(e)}")
