import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import ta
from datetime import datetime, timedelta

# Dictionnaire des actifs disponibles
assets = {
    "EUR/USD (Forex)": "EURUSD=X",
    "Bitcoin (Crypto)": "BTC-USD",
    "Ethereum (Crypto)": "ETH-USD",
    "S&P 500 (Indice)": "^GSPC",
    "Apple (Action)": "AAPL"
}

def run():
    st.title("📊 Analyse Technique Universelle")
    st.markdown("**✅ Sélectionne un actif** (actions, crypto, forex...)")

    actif_choisi = st.selectbox("Choisis un actif", list(assets.keys()))

    if st.button("Analyser"):
        try:
            ticker = assets[actif_choisi]
            fin = datetime.today()
            debut = fin - timedelta(days=90)
            df = yf.download(ticker, start=debut, end=fin)

            if df.empty:
                st.warning("Aucune donnée trouvée pour cet actif.")
                return

            # Calcul des indicateurs
            df["EMA20"] = ta.trend.EMAIndicator(df["Close"], window=20).ema_indicator()
            df["EMA50"] = ta.trend.EMAIndicator(df["Close"], window=50).ema_indicator()
            df["RSI"] = ta.momentum.RSIIndicator(df["Close"], window=14).rsi()

            macd = ta.trend.MACD(df["Close"])
            df["MACD"] = macd.macd()
            df["MACD_SIGNAL"] = macd.macd_signal()

            # Graphique type TradingView avec chandeliers
            fig = go.Figure()
            fig.add_trace(go.Candlestick(
                x=df.index,
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df["Close"],
                name="Cours"
            ))
            fig.add_trace(go.Scatter(x=df.index, y=df["EMA20"], line=dict(width=1), name="EMA 20"))
            fig.add_trace(go.Scatter(x=df.index, y=df["EMA50"], line=dict(width=1), name="EMA 50"))

            fig.update_layout(
                title=f"Données de {actif_choisi}",
                xaxis_title="Date",
                yaxis_title="Prix",
                xaxis_rangeslider_visible=False,
                height=600
            )

            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Erreur lors de l'analyse : {e}")
