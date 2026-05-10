import streamlit as st
from config import THEME

def render_global_header():
    """
    Renders a transparent brand overlay that allows Streamlit's native arrow to function.
    """
    st.markdown(f"""
        <div class='global-header'>
            <div class='logo-container'>
                <div class='logo-img'>A</div>
                <div class='brand-name'>AETHER</div>
            </div>
            <div style='display: flex; gap: 20px; align-items: center;'>
                <div class='nav-hint'>PRO EDITION</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # We remove the custom JS and the spacer div so the header sits 
    # directly over the main content area without blocking native Streamlit elements.
