import streamlit as st
from config import THEME
from state.session_manager import SessionManager

def render_paper_details():
    paper = st.session_state.get("selected_paper")
    
    if not paper:
        st.info("Select a paper from Search or Home to view analysis.")
        return

    # Header Section
    st.markdown(f"""
        <div class='fade-in' style='padding: 40px; background: {THEME["glass"]}; border-radius: 24px; border: 1px solid {THEME["border"]}; margin-bottom: 40px;'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <button onclick='window.location.reload()' style='background: transparent; border: none; color: {THEME["primary_accent"]}; cursor: pointer;'>← Back to Library</button>
                <div class='badge'>PREMIUM ANALYSIS</div>
            </div>
            <h1 style='font-size: 2.8rem; margin-top: 20px; line-height: 1.2;'>{paper['title']}</h1>
            <p style='color: {THEME["text_muted"]}; font-size: 1.1rem;'>Published on {paper['published'][:10]} | Source: arXiv</p>
        </div>
    """, unsafe_allow_html=True)

    col_main, col_side = st.columns([2, 1])

    with col_main:
        st.write("### 📝 Research Abstract")
        st.write(paper['abstract'])
        
        st.write("### 🔑 Semantic Concept Map")
        st.markdown("<div style='display: flex; flex-wrap: wrap; gap: 10px;'>", unsafe_allow_html=True)
        for kw in paper.get('cleaned_keywords', []):
            st.markdown(f"<div class='badge' style='background: {THEME['secondary']}; color: {THEME['text_main']}; border: 1px solid {THEME['border']}'>{kw.upper()}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_side:
        # Actions Panel
        st.markdown(f"""
            <div style='padding: 24px; background: {THEME["secondary"]}; border-radius: 16px; border: 1px solid {THEME["border"]};'>
                <h4 style='margin-top: 0;'>Quick Actions</h4>
                <p style='font-size: 0.8rem; color: {THEME["text_muted"]};'>Manage this paper in your library</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔖 Bookmark this Research", use_container_width=True):
            SessionManager.add_bookmark(paper)
            st.toast("Saved!")

        st.button("📄 Export Citation (BibTeX)", use_container_width=True)
        st.button("🤖 Generate AI Summary", use_container_width=True, type="primary")

        st.write("##")
        st.write("### 🏷 Extraction Highlights")
        for ph in paper.get('important_phrases', []):
            st.markdown(f"- **{ph.title()}**")

    # Clear selection button
    if st.button("Close Analysis View"):
        st.session_state.selected_paper = None
        st.rerun()

if __name__ == "__main__":
    render_paper_details()
