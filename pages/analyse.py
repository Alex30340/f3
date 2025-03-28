import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import ta

def run():
    st.title("📊 Analyse Technique Universelle")

    st.markdown("**📈 Sélectionne un actif (actions, crypto, forex...)**")

    actifs = {
        "Bitcoin (Crypto)": "BTC-USD",
        "Ethereum (Crypto)": "ETH-USD",
        "EUR/USD (Forex)": "EURUSD=X",
        "Apple (Action)": "AAPL",
        "Tesla (Action)": "TSLA",
        "CAC 40 (Indice)": "^FCHI"
    }

    actif_choisi = st.selectbox("Choisis un actif", list(actifs.keys()))
    symbole = actifs[actif_choisi]

    try:
        df = yf.download(symbole, period="3mo", interval="1d")
        if df.empty:
            st.error("❌ Aucune donnée disponible pour cet actif.")
            return

        # Nettoyage & indicateurs
        df.dropna(inplace=True)
        df['SMA20'] = ta.trend.sma_indicator(df['Close'], window=20)
        df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()

        st.subheader(f"📉 Graphique de {actif_choisi}")

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(df.index, df['Close'].values.ravel(), label="Prix de clôture")
        ax.plot(df.index, df['SMA20'].values.ravel(), label="SMA 20j")
        ax.set_title(f"Prix & Moyenne Mobile - {actif_choisi}")
        ax.set_xlabel("Date")
        ax.set_ylabel("Prix")
        ax.legend()
        st.pyplot(fig)

        st.subheader("📍 Indicateur RSI")

        fig2, ax2 = plt.subplots(figsize=(12, 2))
        ax2.plot(df.index, df['RSI'].values.ravel(), color='orange', label="RSI")
        ax2.axhline(70, color='red', linestyle='--', label="Suracheté (70)")
        ax2.axhline(30, color='green', linestyle='--', label="Survendu (30)")
        ax2.set_title("Indice de Force Relative (RSI)")
        ax2.set_ylim([0, 100])
        ax2.legend()
        st.pyplot(fig2)

    except Exception as e:
        st.error(f"❌ Erreur lors du chargement ou de l'analyse : {e}")
