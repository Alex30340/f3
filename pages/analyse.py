# pages/analyse.py — version Streamlit avec tickers universels

import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import ta

def run():
    st.title("Analyse Technique 📊")

    tickers = {
        "EUR/USD": "EURUSD=X",
        "USD/JPY": "USDJPY=X",
        "GBP/USD": "GBPUSD=X",
        "BTC/USD": "BTC-USD",
        "ETH/USD": "ETH-USD",
        "Apple (AAPL)": "AAPL",
        "Tesla (TSLA)": "TSLA",
        "S&P 500": "^GSPC",
        "CAC 40": "^FCHI"
    }

    st.sidebar.subheader("Sélection du ticker")
    choix = st.sidebar.selectbox("Choisissez un actif :", list(tickers.keys()))
    symbol = tickers[choix]

    start = st.sidebar.date_input("Date de début", pd.to_datetime("2024-01-01"))
    end = st.sidebar.date_input("Date de fin", pd.to_datetime("today"))

    data = yf.download(symbol, start=start, end=end)

    if data.empty:
        st.warning("Aucune donnée trouvée pour ce ticker.")
        return

    st.subheader(f"Graphique de {symbol}")
    fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close']
    )])
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Indicateurs techniques")
    data["EMA20"] = ta.trend.ema_indicator(data["Close"], window=20)
    data["RSI"] = ta.momentum.RSIIndicator(data["Close"]).rsi()

    st.line_chart(data[["Close", "EMA20"]])
    st.line_chart(data["RSI"])
