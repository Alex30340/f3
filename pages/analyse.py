# pages/analyse.py — version Streamlit

import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import ta

def run():
    st.title("Analyse Technique 📊")

    st.sidebar.subheader("Sélection de la paire")
    pair = st.sidebar.selectbox("Choisir une paire :", ["EURUSD", "GBPUSD", "USDJPY", "BTC-USD", "ETH-USD"])
    start = st.sidebar.date_input("Date de début", pd.to_datetime("2024-01-01"))
    end = st.sidebar.date_input("Date de fin", pd.to_datetime("today"))

    data = yf.download(pair, start=start, end=end)
    if data.empty:
        st.warning("Aucune donnée trouvée pour cette période.")
        return

    st.subheader(f"Graphique de {pair}")
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
