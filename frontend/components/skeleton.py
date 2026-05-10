import streamlit as st

def render_paper_skeleton():
    """
    Renders a shimmer effect skeleton for paper cards during loading.
    """
    st.markdown("""
        <div class='paper-card shimmer-bg' style='height: 250px; margin-bottom: 20px; opacity: 0.5;'>
            <div style='width: 30%; height: 20px; background: rgba(255,255,255,0.05); border-radius: 4px; margin-bottom: 15px;'></div>
            <div style='width: 80%; height: 30px; background: rgba(255,255,255,0.05); border-radius: 4px; margin-bottom: 10px;'></div>
            <div style='width: 60%; height: 20px; background: rgba(255,255,255,0.05); border-radius: 4px; margin-bottom: 25px;'></div>
            <div style='width: 100%; height: 80px; background: rgba(255,255,255,0.05); border-radius: 4px;'></div>
        </div>
    """, unsafe_allow_html=True)

def render_metric_skeleton():
    """
    Renders shimmers for dashboard metrics.
    """
    st.markdown("""
        <div class='shimmer-bg' style='height: 100px; border-radius: 20px; opacity: 0.3;'></div>
    """, unsafe_allow_html=True)
