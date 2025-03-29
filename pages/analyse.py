import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ta.trend import MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands

def run():
    st.title("📊 Analyse Technique Universelle")
    st.markdown("**✅ Sélectionne un actif (actions, crypto, forex...)**")

    actifs = {
        "Bitcoin (Crypto)": "BTC-USD",
        "Ethereum (Crypto)": "ETH-USD",
        "EUR/USD (Forex)": "EURUSD=X",
        "Apple (Stock)": "AAPL",
        "Tesla (Stock)": "TSLA"
    }

    choix = st.selectbox("Choisis un actif", list(actifs.keys()))

    try:
        ticker = actifs[choix]
        df = yf.download(ticker, period="3mo", interval="1d")
        df.dropna(inplace=True)

        st.write(f"### Données de {choix}")
        st.line_chart(df["Close"])

        # Correction ici : s'assurer que les données sont en 1D
        close = df["Close"]

        # MACD
        macd = MACD(close=close).macd()
        signal = MACD(close=close).macd_signal()

        # RSI
        rsi = RSIIndicator(close=close).rsi()

        # Bollinger
        bollinger = BollingerBands(close=close)
        bb_high = bollinger.bollinger_hband()
        bb_low = bollinger.bollinger_lband()

        st.write("### Indicateurs Techniques")

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(df.index, close, label="Prix de clôture")
        ax.plot(df.index, bb_high, label="Bollinger High", linestyle="--")
        ax.plot(df.index, bb_low, label="Bollinger Low", linestyle="--")
        ax.set_title("Bollinger Bands")
        ax.legend()
        st.pyplot(fig)

        st.write("#### MACD")
        st.line_chart(pd.DataFrame({"MACD": macd, "Signal": signal}, index=df.index))

        st.write("#### RSI")
        st.line_chart(pd.DataFrame({"RSI": rsi}, index=df.index))

    except Exception as e:
        st.error(f"❌ Erreur lors du chargement ou de l'analyse : {e}")
