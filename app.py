import streamlit as st

# ✅ Cette ligne doit être la toute première commande Streamlit
st.set_page_config(page_title="Forex Analyzer", layout="wide")

from pages import analyse, dashboard, backtest, education, lab

# Dictionnaire de navigation
pages = {
    "Analyse Technique": analyse.run,
    "Portefeuille": dashboard.run,
    "Backtest": backtest.run,
    "Éducation": education.run,
    "LAB": lab.run
}

# Menu latéral
st.sidebar.title("Navigation")
choix = st.sidebar.radio("Aller vers :", list(pages.keys()))
pages[choix]()
