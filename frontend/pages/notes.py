import streamlit as st
from config import THEME
from state.session_manager import SessionManager

def render_notes():
    st.write("# My Research Notes")
    
    notes = SessionManager.get(SessionManager.USER, "notes")
    
    if not notes:
        st.markdown(f"""
            <div style='text-align: center; padding: 100px 0;'>
                <div style='font-size: 5rem; margin-bottom: 20px;'>📝</div>
                <h3>Your notebook is empty.</h3>
                <p style='color: {THEME["text_muted"]};'>Take notes on papers during your analysis to see them here.</p>
            </div>
        """, unsafe_allow_html=True)
        return

    st.write(f"### You have {len(notes)} annotated papers")
    
    for paper_url, note_content in notes.items():
        with st.expander(f"📌 Note on Paper: {paper_url}"):
            st.text_area("Note Content", value=note_content, height=150, key=f"note_{paper_url}")
            if st.button("Delete Note", key=f"del_{paper_url}"):
                del notes[paper_url]
                SessionManager.set(SessionManager.USER, "notes", notes)
                st.toast("Note deleted")
                st.rerun()

    if st.button("Export All Notes as Markdown"):
        st.toast("Exporting...")
        # Export logic placeholder
        
if __name__ == "__main__":
    render_notes()
