import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import ta

def run():
    st.title("📊 Analyse Technique Universelle")
    st.markdown("✅ **Sélectionne un actif** (actions, crypto, forex...)")

    actifs = {
        "Bitcoin (Crypto)": "BTC-USD",
        "Ethereum (Crypto)": "ETH-USD",
        "Apple (Action)": "AAPL",
        "EUR/USD (Forex)": "EURUSD=X",
        "Gold (Matière Première)": "GC=F"
    }

    choix = st.selectbox("Choisis un actif", list(actifs.keys()))
    ticker = actifs[choix]

    if st.button("Analyser"):
        try:
            df = yf.download(ticker, period="3mo", interval="1d")
            df.dropna(inplace=True)

            # Calcul des indicateurs
            df["EMA20"] = ta.trend.ema_indicator(df["Close"], window=20)
            df["EMA50"] = ta.trend.ema_indicator(df["Close"], window=50)

            macd = ta.trend.macd(df["Close"])
            df["MACD"] = macd.macd()
            df["MACD_SIGNAL"] = macd.macd_signal()

            df["RSI"] = ta.momentum.RSIIndicator(df["Close"]).rsi()

            # Détection des supports/résistances
            supports = df["Low"].rolling(window=5).min()
            resistances = df["High"].rolling(window=5).max()

            # Graphique en bougies japonaises avec Plotly
            fig = go.Figure()

            fig.add_trace(go.Candlestick(
                x=df.index,
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df["Close"],
                name="Prix",
            ))

            # Lignes EMA
            fig.add_trace(go.Scatter(x=df.index, y=df["EMA20"], mode="lines", name="EMA 20"))
            fig.add_trace(go.Scatter(x=df.index, y=df["EMA50"], mode="lines", name="EMA 50"))

            # Supports & résistances (simplifiés)
            fig.add_trace(go.Scatter(x=df.index, y=supports, mode="lines", name="Support", line=dict(dash="dot")))
            fig.add_trace(go.Scatter(x=df.index, y=resistances, mode="lines", name="Résistance", line=dict(dash="dot")))

            fig.update_layout(
                title=f"Données de {choix}",
                xaxis_rangeslider_visible=False,
                template="plotly_white",
                height=600
            )

            st.plotly_chart(fig, use_container_width=True)

            # Indicateurs additionnels
            with st.expander("📈 Indicateurs techniques"):
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("RSI")
                    st.line_chart(df["RSI"])

                with col2:
                    st.subheader("MACD")
                    st.line_chart(df[["MACD", "MACD_SIGNAL"]])

        except Exception as e:
            st.error(f"Erreur lors de l'analyse : {e}")
