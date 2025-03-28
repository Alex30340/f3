
import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import ta

def run():
    st.title("Analyse Technique Universelle")
    st.write("📊 Sélectionne un actif (actions, crypto, forex...)")

    symboles = {
        "EUR/USD (Forex)": "EURUSD=X",
        "Bitcoin (Crypto)": "BTC-USD",
        "Apple (Action)": "AAPL",
        "CAC 40 (Indice)": "^FCHI",
        "Or (Gold)": "GC=F",
        "USD/JPY (Forex)": "JPY=X",
        "Ethereum (Crypto)": "ETH-USD"
    }

    actif = st.selectbox("Choisis un actif", list(symboles.keys()))
    ticker = symboles[actif]

    try:
        data = yf.download(ticker, period="3mo", interval="1d")
        if data.empty:
            st.error("❌ Aucune donnée trouvée pour ce symbole.")
            return

        data["EMA20"] = ta.trend.EMAIndicator(close=data["Close"], window=20).ema_indicator()
        data["RSI"] = ta.momentum.RSIIndicator(close=data["Close"], window=14).rsi()

        st.write(f"### Données de {actif}")
        st.line_chart(data[["Close", "EMA20"]])

        st.write("### RSI")
        fig, ax = plt.subplots()
        ax.plot(data["RSI"])
        ax.axhline(70, color='red', linestyle='--')
        ax.axhline(30, color='green', linestyle='--')
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Erreur lors du chargement ou de l'analyse : {e}")
