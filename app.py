# app.py — version Streamlit

import streamlit as st
from pages import analyse, dashboard, backtest, education, lab

st.set_page_config(page_title="Forex Analyzer", layout="wide")

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
import os
os.environ["PORT"] = "10000"
