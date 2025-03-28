# app_instance.py - version Streamlit
import streamlit as st

def app():
    st.set_page_config(page_title="Forex Analyzer", layout="wide")

    st.title("Bienvenue sur Forex Analyzer")
    st.write("Ceci est le cœur de l'application.")
