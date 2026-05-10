import streamlit as st
from config import THEME
from state.session_manager import SessionManager

def render_hero():
    st.markdown(f"""
        <div class='fade-in' style='text-align: center; padding: 100px 20px; background: radial-gradient(circle at top right, rgba(124, 58, 237, 0.1), transparent), radial-gradient(circle at bottom left, rgba(37, 99, 235, 0.1), transparent); border-radius: 30px; border: 1px solid {THEME["border"]}; margin-bottom: 60px;'>
            <h1 style='font-size: 4rem; background: linear-gradient(to right, #F8FAFC, #94A3B8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 20px; line-height: 1.1;'>
                The Future of Scientific <br/> Intelligence is Here.
            </h1>
            <p style='font-size: 1.25rem; color: {THEME["text_muted"]}; max-width: 800px; margin: 0 auto 40px;'>
                Aether processes millions of data points to deliver high-fidelity insights, 
                automated literature reviews, and trend forecasts for the modern researcher.
            </p>
            <div style='display: flex; justify-content: center; gap: 16px;'>
                <a href='Search' target='_self' style='text-decoration: none; background: {THEME["primary_accent"]}; color: white; padding: 14px 32px; border-radius: 12px; font-weight: 700; box-shadow: {THEME["glow_primary"]};'>Start Discovery</a>
                <a href='Dashboard' target='_self' style='text-decoration: none; background: {THEME["secondary"]}; color: white; padding: 14px 32px; border-radius: 12px; font-weight: 700; border: 1px solid {THEME["border"]};'>Intelligence Dashboard</a>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_home():
    render_hero()
    
    # Stats Grid
    stats = SessionManager.get(SessionManager.DATA, "stats")
    
    col1, col2, col3, col4 = st.columns(4)
    metric_style = f"background: {THEME['glass']}; border: 1px solid {THEME['border']}; padding: 24px; border-radius: 20px; text-align: center;"
    
    with col1:
        st.markdown(f"<div style='{metric_style}'><h2 style='color: {THEME['primary_accent']}; margin: 0;'>{stats.get('total_papers', 0):,}</h2><p style='color: {THEME['text_muted']}; font-size: 0.8rem; margin: 0;'>Papers Analyzed</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div style='{metric_style}'><h2 style='color: {THEME['secondary_accent']}; margin: 0;'>4.2s</h2><p style='color: {THEME['text_muted']}; font-size: 0.8rem; margin: 0;'>Avg Processing Time</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div style='{metric_style}'><h2 style='color: {THEME['highlight']}; margin: 0;'>12k</h2><p style='color: {THEME['text_muted']}; font-size: 0.8rem; margin: 0;'>Concepts Mapped</p></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div style='{metric_style}'><h2 style='color: #10b981; margin: 0;'>99.9%</h2><p style='color: {THEME['text_muted']}; font-size: 0.8rem; margin: 0;'>System Uptime</p></div>", unsafe_allow_html=True)

    st.write("##")
    
    # Featured Content
    st.write("### 🚀 Emerging Research Trends")
    papers = SessionManager.get(SessionManager.DATA, "papers")[:6]
    
    from components.paper_card import render_paper_card
    
    cols = st.columns(3)
    for i, paper in enumerate(papers):
        with cols[i % 3]:
            render_paper_card(paper, key=f"home_{i}")

if __name__ == "__main__":
    render_home()
