import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from ta.trend import MACD

# Fonction principale

def run():
    st.title("📊 Analyse Technique Universelle")
    st.markdown("""
    #### ✅ Sélectionne un actif *(actions, crypto, forex...)*
    """)

    actifs = {
        "Bitcoin (Crypto)": "BTC-USD",
        "Ethereum (Crypto)": "ETH-USD",
        "EUR/USD (Forex)": "EURUSD=X",
        "USD/JPY (Forex)": "JPY=X",
        "Tesla (Action)": "TSLA",
        "Apple (Action)": "AAPL"
    }

    choix_actif = st.selectbox("Choisis un actif", list(actifs.keys()))
    symbole = actifs[choix_actif]

    if st.button("Analyser"):
        try:
            df = yf.download(symbole, period="3mo")
            df = df.dropna()

            # Calcul MACD
            macd = MACD(close=df["Close"])
            df["MACD"] = macd.macd()
            df["Signal"] = macd.macd_signal()
            df["Histogram"] = macd.macd_diff()

            # Affichage graphique chandeliers avec Plotly
            st.subheader(f"Données de {choix_actif}")

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

            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Prix",
                xaxis_rangeslider_visible=False,
                template="plotly_white",
                height=600
            )

            st.plotly_chart(fig, use_container_width=True)

            st.subheader("MACD")
            st.line_chart(df[["MACD", "Signal"]])

        except Exception as e:
            st.error(f"Erreur lors de l'analyse : {e}")
