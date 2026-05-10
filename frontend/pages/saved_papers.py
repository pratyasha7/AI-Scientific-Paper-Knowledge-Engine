import streamlit as st
from config import THEME
from state.session_manager import SessionManager
from components.paper_card import render_paper_card

def render_saved():
    st.write("# My Research Library")
    
    bookmarks = SessionManager.get(SessionManager.USER, "bookmarks")
    
    if not bookmarks:
        st.markdown(f"""
            <div style='text-align: center; padding: 100px 0;'>
                <div style='font-size: 5rem; margin-bottom: 20px;'>🔖</div>
                <h3>Your library is waiting.</h3>
                <p style='color: {THEME["text_muted"]};'>Save papers from the Discovery feed to build your collection.</p>
                <br/>
                <a href='Search' target='_self' style='text-decoration: none; background: {THEME["primary_accent"]}; color: white; padding: 12px 24px; border-radius: 8px;'>Go to Search</a>
            </div>
        """, unsafe_allow_html=True)
        return

    # Library Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"### {len(bookmarks)} Saved Papers")
    with col2:
        if st.button("Clear All", type="secondary", use_container_width=True):
            SessionManager.set(SessionManager.USER, "bookmarks", [])
            st.rerun()

    st.write("##")

    # Grid Rendering
    for i, paper in enumerate(bookmarks):
        render_paper_card(paper, key=f"saved_{i}")

if __name__ == "__main__":
    render_saved()
