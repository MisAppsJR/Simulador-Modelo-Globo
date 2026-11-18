import streamlit as st
import streamlit.components.v1 as components
from motor_canvas import obtener_html_simulador

st.set_page_config(page_title="Simulador del Globo", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
        html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
            background-color: #060911 !important;
        }
        .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }
        header, footer, [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] {
            display: none !important;
        }
        iframe {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100dvh !important;
            border: none !important;
            margin: 0 !important;
            padding: 0 !important;
            z-index: 9999 !important;
        }
    </style>
""", unsafe_allow_html=True)

components.html(obtener_html_simulador(), height=820, scrolling=False)
