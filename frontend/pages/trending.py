import streamlit as st
from config import THEME
from state.session_manager import SessionManager
from components.paper_card import render_paper_card

def render_trending():
    st.write("# Trending Intelligence")
    st.write("### High-velocity concepts and viral research papers.")
    
    # 1. Concept Cloud
    st.write("##")
    st.write("### 🚀 Emerging Concepts")
    from services.mongo_service import MongoService
    mongo = MongoService()
    trending_keywords = mongo.get_trending_keywords(15)
    
    st.markdown("<div style='display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 40px;'>", unsafe_allow_html=True)
    for kw in trending_keywords:
        st.markdown(f"""
            <div style='background: {THEME["glass"]}; color: {THEME["primary_accent"]}; padding: 10px 24px; border-radius: 30px; font-weight: 700; border: 1px solid {THEME["border"]}; box-shadow: {THEME["glow_primary"]};'>
                {kw['_id'].upper()} <span style='color: {THEME["text_muted"]}; font-size: 0.8rem; margin-left: 8px;'>{kw['count']}</span>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 2. Viral Papers
    st.write("### 📈 Top Momentum Papers")
    papers = SessionManager.get(SessionManager.DATA, "papers")
    viral_papers = sorted(papers, key=lambda x: len(x.get('cleaned_keywords', [])) + len(x.get('important_phrases', [])), reverse=True)[:10]
    
    for i, p in enumerate(viral_papers):
        render_paper_card(p, key=f"trending_{i}")

if __name__ == "__main__":
    render_trending()
