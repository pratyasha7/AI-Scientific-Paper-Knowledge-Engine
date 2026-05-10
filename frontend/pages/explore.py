import streamlit as st
import random
from config import THEME
from state.session_manager import SessionManager
from components.paper_card import render_paper_card

def render_explore():
    st.write("# Explore Research")
    st.write("### Discover curated insights across the research graph.")
    
    papers = SessionManager.get(SessionManager.DATA, "papers")
    if not papers:
        st.warning("No data available to explore.")
        return

    st.markdown("<div class='data-panel'>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["✨ AI Recommended", "🔥 Trending Now", "🆕 Newest Releases"])
    
    with tab1:
        st.write("##")
        # Shuffle for discovery feel
        rec_papers = random.sample(papers, min(9, len(papers)))
        cols = st.columns(3)
        for i, p in enumerate(rec_papers):
            with cols[i % 3]:
                render_paper_card(p, key=f"explore_rec_{i}")

    with tab2:
        st.write("##")
        # Trending based on complexity/phrase count
        trending = sorted(papers, key=lambda x: len(x.get('important_phrases', [])), reverse=True)[:12]
        cols = st.columns(3)
        for i, p in enumerate(trending):
            with cols[i % 3]:
                render_paper_card(p, key=f"explore_trend_{i}")

    with tab3:
        st.write("##")
        newest = sorted(papers, key=lambda x: x.get('published', ''), reverse=True)[:12]
        cols = st.columns(3)
        for i, p in enumerate(newest):
            with cols[i % 3]:
                render_paper_card(p, key=f"explore_new_{i}")
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    render_explore()
