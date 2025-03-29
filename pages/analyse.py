import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from ta.trend import MACD

# Doit être la première commande Streamlit
st.set_page_config(page_title="Analyse Technique", layout="wide")

# Dictionnaire des actifs disponibles
assets = {
    "Bitcoin (Crypto)": "BTC-USD",
    "Ethereum (Crypto)": "ETH-USD",
    "EUR/USD (Forex)": "EURUSD=X",
    "USD/JPY (Forex)": "JPY=X",
    "Tesla (Action)": "TSLA",
    "Apple (Action)": "AAPL"
}

def run():
    st.title("📊 Analyse Technique Universelle")
    st.markdown("✅ **Sélectionne un actif** *(actions, crypto, forex...)*")

    actif = st.selectbox("Choisis un actif", list(assets.keys()))
    ticker = assets[actif]

    if st.button("Analyser"):
        try:
            df = yf.download(ticker, period="3mo", interval="1d")

            if df.empty:
                st.error("Aucune donnée disponible pour cet actif.")
                return

            df.dropna(inplace=True)
            df.reset_index(inplace=True)

            # Affichage du graphique en chandeliers (TradingView-style)
            fig = go.Figure(data=[go.Candlestick(
                x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name="Prix"
            )])
            fig.update_layout(title=f"📈 Données de {actif}", xaxis_rangeslider_visible=False)

            st.plotly_chart(fig, use_container_width=True)

            # --- Analyse technique : MACD ---
            macd = MACD(close=df['Close'])
            df['MACD'] = macd.macd()
            df['Signal'] = macd.macd_signal()

            fig_macd = go.Figure()
            fig_macd.add_trace(go.Scatter(x=df['Date'], y=df['MACD'], mode='lines', name='MACD'))
            fig_macd.add_trace(go.Scatter(x=df['Date'], y=df['Signal'], mode='lines', name='Signal'))
            fig_macd.update_layout(title="📊 MACD", xaxis_title="Date", yaxis_title="Valeur")

            st.plotly_chart(fig_macd, use_container_width=True)

        except Exception as e:
            st.error(f"Erreur lors de l'analyse : {e}")
