import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import ta
import pandas as pd

def run():
    st.title("📊 Analyse Technique Universelle")
    st.markdown("### ✅ Sélectionne un actif *(actions, crypto, forex...)*")

    actifs = {
        "Bitcoin (Crypto)": "BTC-USD",
        "Ethereum (Crypto)": "ETH-USD",
        "EUR/USD (Forex)": "EURUSD=X",
        "USD/JPY (Forex)": "JPY=X",
        "S&P 500 (Indice)": "^GSPC",
        "Apple (Action)": "AAPL",
        "Tesla (Action)": "TSLA",
    }

    choix = st.selectbox("Choisis un actif", list(actifs.keys()))
    symbole = actifs[choix]

    if st.button("Analyser"):
        try:
            df = yf.download(symbole, period="3mo", interval="1d")
            df.dropna(inplace=True)

            # ✅ Forcer les colonnes à être plates (1D Series)
            for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
                df[col] = df[col].astype(float).squeeze()

            # ✅ Ajout indicateurs techniques
            df['RSI'] = ta.momentum.RSIIndicator(close=df['Close']).rsi()
            macd = ta.trend.MACD(close=df['Close'])
            df['MACD'] = macd.macd()
            df['Signal'] = macd.macd_signal()

            # ✅ Graphique type TradingView (bougies)
            fig = go.Figure(data=[
                go.Candlestick(
                    x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'],
                    name="Prix"
                )
            ])
            fig.update_layout(title=f"Graphique de {choix}", xaxis_title="Date", yaxis_title="Prix")

            st.plotly_chart(fig, use_container_width=True)

            # ✅ RSI & MACD
            st.subheader("📈 Indicateurs Techniques")

            col1, col2 = st.columns(2)

            with col1:
                st.line_chart(df[['RSI']].dropna(), use_container_width=True)
            with col2:
                st.line_chart(df[['MACD', 'Signal']].dropna(), use_container_width=True)

        except Exception as e:
            st.error(f"Erreur lors de l'analyse : {e}")
