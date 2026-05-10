import streamlit as st
from state.session_manager import SessionManager

def render_paper_card(paper: dict, score: int = None, key: str = None):
    """
    Renders a premium paper card with SaaS actions and stateful interactions.
    """
    title = paper.get('title', 'Untitled')
    abstract = paper.get('abstract', 'No abstract available.')
    published = paper.get('published', 'N/A')[:10]
    url = paper.get('url', '#')
    keywords = paper.get('cleaned_keywords', [])[:3]
    
    # Bookmark State
    bookmarks = SessionManager.get(SessionManager.USER, "bookmarks")
    is_bookmarked = any(b.get('url') == url for b in bookmarks)
    
    st.markdown(f"""
        <div class='paper-card fade-in'>
            <div style='display: flex; justify-content: space-between; align-items: flex-start;'>
                <div style='flex: 1;'>
                    <div class='badge neon-border' style='margin-bottom: 12px; background: rgba(0, 210, 255, 0.1); color: #00d2ff;'>INTELLIGENCE NODE</div>
                    <h3 class='card-title'>{title}</h3>
                </div>
                {f"<div class='badge' style='background: rgba(124, 58, 237, 0.1); color: #7C3AED; border: 1px solid rgba(124, 58, 237, 0.2);'>Relevance: {score}%</div>" if score else ""}
            </div>
            
            <div class='card-metadata'>
                <span>📅 {published}</span>
                <span>🔗 <a href='{url}' target='_blank' style='color: var(--secondary-accent); text-decoration: none;'>View Source</a></span>
            </div>
            
            <p class='card-abstract'>{abstract[:280]}...</p>
            
            <div style='display: flex; gap: 8px; margin-top: 15px;'>
                {''.join([f"<span class='badge' style='background: var(--bg-secondary); color: var(--text-muted); border: none;'>{kw}</span>" for kw in keywords])}
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Action Buttons (Stateful)
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        if st.button("🔖" if not is_bookmarked else "⭐", key=f"bk_{key}", help="Save to bookmarks"):
            if is_bookmarked:
                SessionManager.remove_bookmark(paper)
                st.toast("Removed from bookmarks")
            else:
                SessionManager.add_bookmark(paper)
                st.toast("Saved to bookmarks", icon="⭐")
            st.rerun()
            
    with col2:
        if st.button("📊", key=f"det_{key}", help="Analyze Paper"):
            st.session_state.selected_paper = paper
            st.rerun()
            
    with col3:
        # Quick summary placeholder
        action_col1, action_col2 = st.columns(2)
        with action_col1:
            if st.button("AI Summary", key=f"ai_{key}", use_container_width=True):
                st.toast("Summarizing...", icon="🤖")
        with action_col2:
            if st.button("🔗 Share", key=f"share_{key}", use_container_width=True):
                st.write(f"Copy link: `{url}`")
                st.toast("Link displayed below card")
