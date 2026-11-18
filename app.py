import streamlit as st
import streamlit.components.v1 as components
from motor_canvas import obtener_html_simulador

st.set_page_config(page_title="Simulador del Globo", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
        .block-container { padding: 0 !important; max-width: 100% !important; }
        header, footer, [data-testid="stToolbar"] { display: none !important; }
        iframe { height: 100dvh !important; min-height: 520px; width: 100% !important; display: block; }
    </style>
""", unsafe_allow_html=True)

components.html(obtener_html_simulador(), height=820, scrolling=False)
