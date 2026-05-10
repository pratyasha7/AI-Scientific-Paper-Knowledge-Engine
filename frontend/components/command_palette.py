import streamlit as st
from state.session_manager import SessionManager

def render_command_palette():
    """
    Renders a floating command palette (triggered by UI or potentially JS).
    For Streamlit, we use a dialog/modal approach.
    """
    if "show_command_palette" not in st.session_state:
        st.session_state.show_command_palette = False

    # Keyboard shortcut listener placeholder (requires custom JS for real Cmd+K)
    st.markdown("""
        <script>
            document.addEventListener('keydown', function(e) {
                if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
                    e.preventDefault();
                    // Custom Streamlit event trigger would go here
                }
            });
        </script>
    """, unsafe_allow_html=True)

    if st.sidebar.button("⌨️ Command Palette (Ctrl+K)", use_container_width=True):
        st.session_state.show_command_palette = True

    if st.session_state.show_command_palette:
        with st.expander("🚀 Quick Actions", expanded=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                cmd_query = st.text_input("Run command or search...", placeholder="e.g. 'go to search', 'clear bookmarks'...")
            with col2:
                st.write("##")
                if st.button("Close"):
                    st.session_state.show_command_palette = False
                    st.rerun()

            if cmd_query:
                # Basic Command Router
                q = cmd_query.lower()
                if "search" in q:
                    st.success("Redirecting to Search...")
                    # Page redirection logic
                elif "clear" in q and "bookmark" in q:
                    SessionManager.set(SessionManager.USER, "bookmarks", [])
                    st.toast("Bookmarks cleared!")
                elif "theme" in q:
                    st.info("Theme settings can be adjusted in Settings page.")
                else:
                    st.write("No command matched. Try 'go to dashboard' or 'search transformers'.")
