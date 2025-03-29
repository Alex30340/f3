import streamlit as st

# La toute première commande du fichier
st.set_page_config(page_title="Forex Analyzer", layout="wide")

from pages import analyse, dashboard, backtest, education, lab

pages = {
    "Analyse Technique": analyse.run,
    "Portefeuille": dashboard.run,
    "Backtest": backtest.run,
    "Éducation": education.run,
    "LAB": lab.run
}

st.sidebar.title("Navigation")
choix = st.sidebar.radio("Aller vers :", list(pages.keys()))
pages[choix]()
