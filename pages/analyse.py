import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import ta

st.set_page_config(page_title="Analyse Technique", layout="wide")

def detect_support_resistance(df, window=5):
    support = []
    resistance = []
    for i in range(window, len(df) - window):
        is_support = all(df['Low'].iloc[i] < df['Low'].iloc[i - j] for j in range(1, window)) and \
                     all(df['Low'].iloc[i] < df['Low'].iloc[i + j] for j in range(1, window))
        is_resistance = all(df['High'].iloc[i] > df['High'].iloc[i - j] for j in range(1, window)) and \
                        all(df['High'].iloc[i] > df['High'].iloc[i + j] for j in range(1, window))
        if is_support:
            support.append((df.index[i], df['Low'].iloc[i]))
        if is_resistance:
            resistance.append((df.index[i], df['High'].iloc[i]))
    return support, resistance

def run():
    st.title("📊 Analyse Technique Universelle")
    st.markdown("✅ **Sélectionne un actif** (_actions, crypto, forex..._)")

    actifs = {
        "Bitcoin (Crypto)": "BTC-USD",
        "Ethereum (Crypto)": "ETH-USD",
        "BNB (Crypto)": "BNB-USD",
        "EUR/USD (Forex)": "EURUSD=X",
        "USD/JPY (Forex)": "JPY=X",
        "Tesla (Action)": "TSLA",
        "Apple (Action)": "AAPL",
        "Microsoft (Action)": "MSFT",
        "Amazon (Action)": "AMZN",
        "S&P 500": "^GSPC"
    }

    actif_nom = st.selectbox("Choisis un actif", list(actifs.keys()))
    symbole = actifs[actif_nom]

    if st.button("Analyser"):
        try:
            df = yf.download(symbole, period="3mo", interval="1d")
            if df.empty:
                st.error("Aucune donnée disponible.")
                return

            df['EMA20'] = ta.trend.ema_indicator(df['Close'], window=20)
            df['EMA50'] = ta.trend.ema_indicator(df['Close'], window=50)
            macd = ta.trend.macd(df['Close'])
            df['MACD'] = macd.macd()
            df['MACD_signal'] = macd.macd_signal()
            df['RSI'] = ta.momentum.RSIIndicator(df['Close']).rsi()

            support_lines, resistance_lines = detect_support_resistance(df)

            fig = go.Figure()

            fig.add_trace(go.Candlestick(
                x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name='Bougies'
            ))

            fig.add_trace(go.Scatter(x=df.index, y=df['EMA20'], mode='lines', name='EMA20'))
            fig.add_trace(go.Scatter(x=df.index, y=df['EMA50'], mode='lines', name='EMA50'))

            for s in support_lines:
                fig.add_hline(y=s[1], line_dash="dot", line_color="green", annotation_text="Support")

            for r in resistance_lines:
                fig.add_hline(y=r[1], line_dash="dot", line_color="red", annotation_text="Résistance")

            # TP/SL fictifs à partir du dernier prix
            last_price = df['Close'].iloc[-1]
            tp = round(last_price * 1.05, 2)
            sl = round(last_price * 0.95, 2)
            risk = round(last_price - sl, 2)
            reward = round(tp - last_price, 2)
            rr_ratio = round(reward / risk, 2)

            fig.add_hline(y=tp, line_color="blue", annotation_text="Take Profit", line_dash="dash")
            fig.add_hline(y=sl, line_color="orange", annotation_text="Stop Loss", line_dash="dash")

            st.subheader(f"Données de {actif_nom}")
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(f"💡 **Risk/Reward Ratio** : `{rr_ratio}` | 🎯 **TP**: {tp} | 🛑 **SL**: {sl}")

            st.markdown("### 🔎 Indicateurs")
            col1, col2 = st.columns(2)
            col1.metric("RSI", round(df['RSI'].iloc[-1], 2))
            col2.metric("MACD", round(df['MACD'].iloc[-1], 2))

        except Exception as e:
            st.error(f"Erreur : {e}")
