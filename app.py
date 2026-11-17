import streamlit as st
import streamlit.components.v1 as components
from motor_canvas import obtener_html_simulador

st.set_page_config(page_title="Simulador del Globo", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
        .block-container { padding-top: 0.4rem; padding-bottom: 0rem; padding-left: 0.5rem; padding-right: 0.5rem; max-width: 100%; }
        header { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

components.html(obtener_html_simulador(), height=810, scrolling=False)
