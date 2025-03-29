import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import ta

st.markdown("## 📊 Analyse Technique Universelle")
st.markdown("### ✅ Sélectionne un actif *(actions, crypto, forex...)*")

# Liste d'exemples d'actifs
actifs = {
    "Bitcoin (Crypto)": "BTC-USD",
    "Ethereum (Crypto)": "ETH-USD",
    "Tesla (Action)": "TSLA",
    "Apple (Action)": "AAPL",
    "EUR/USD (Forex)": "EURUSD=X",
    "USD/JPY (Forex)": "JPY=X",
    "Or (Gold)": "GC=F"
}

choix_actif = st.selectbox("Choisis un actif", list(actifs.keys()))
symbole = actifs[choix_actif]

if st.button("Analyser"):
    try:
        # Téléchargement des données
        df = yf.download(symbole, period="3mo", interval="1d")

        if df.empty:
            st.error("Aucune donnée disponible pour cet actif.")
        else:
            # Sécurité : forcer toutes les colonnes à être 1D
            df['Open'] = pd.Series(df['Open'].values.squeeze(), index=df.index)
            df['High'] = pd.Series(df['High'].values.squeeze(), index=df.index)
            df['Low'] = pd.Series(df['Low'].values.squeeze(), index=df.index)
            df['Close'] = pd.Series(df['Close'].values.squeeze(), index=df.index)
            df['Volume'] = pd.Series(df['Volume'].values.squeeze(), index=df.index)

            df.dropna(inplace=True)

            st.subheader(f"Données de {choix_actif}")

            # Candlestick Chart
            fig = go.Figure(data=[
                go.Candlestick(
                    x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'],
                    name='Bougies'
                )
            ])
            fig.update_layout(xaxis_rangeslider_visible=False, height=500)
            st.plotly_chart(fig, use_container_width=True)

            # MACD
            df['macd'] = ta.trend.macd(df['Close'])
            df['macd_signal'] = ta.trend.macd_signal(df['Close'])

            st.line_chart(df[['macd', 'macd_signal']].dropna())

    except Exception as e:
        st.error(f"Erreur lors de l'analyse : {e}")
