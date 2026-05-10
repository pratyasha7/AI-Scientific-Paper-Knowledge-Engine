import os
import streamlit as st

# Application Identity
APP_NAME = "AETHER"
APP_TAGLINE = "Research Intelligence Platform"
VERSION = "3.0.0-PREMIUM"

# Premium SaaS Palette (Base: #050816)
THEME = {
    "base": "#050816",
    "secondary": "#0B1020",
    "surface": "#111827",
    "card": "rgba(17, 24, 39, 0.72)",
    "glass": "rgba(15, 23, 42, 0.58)",
    "border": "rgba(255, 255, 255, 0.08)",
    "primary_accent": "#7C3AED",    # Purple
    "secondary_accent": "#2563EB",  # Blue
    "highlight": "#06B6D4",         # Cyan
    "text_main": "#F8FAFC",
    "text_muted": "#94A3B8",
    "glow_primary": "0 0 20px rgba(124, 58, 237, 0.4)",
    "glow_secondary": "0 0 20px rgba(37, 99, 235, 0.4)",
    "shadow_premium": "0 10px 40px -10px rgba(0, 0, 0, 0.5)"
}

# Typography
FONTS = {
    "primary": "Inter, sans-serif",
    "display": "Manrope, sans-serif",
    "accent": "Sora, sans-serif"
}

# Paths
BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
STYLES_DIR = os.path.join(BASE_DIR, "styles")

def init_page_config():
    st.set_page_config(
        page_title=f"{APP_NAME} | {APP_TAGLINE}",
        page_icon="🧬",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def inject_custom_css():
    """Injects granular CSS files from the styles/ directory."""
    css_files = [
        "global.css", "theme.css", "animations.css", "cards.css", 
        "sidebar.css", "navbar.css", "forms.css", "buttons.css", 
        "layout.css", "typography.css"
    ]
    for css_file in css_files:
        path = os.path.join(STYLES_DIR, css_file)
        if os.path.exists(path):
            with open(path) as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
