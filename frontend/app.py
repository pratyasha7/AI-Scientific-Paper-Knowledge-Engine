import streamlit as st
import time
from config import init_page_config, inject_custom_css, THEME
from state.session_manager import SessionManager
from services.mongo_service import MongoService
from services.search_service import SearchService

# 1. Initialize Page & Style
init_page_config()
inject_custom_css()

# 2. Initialize State
SessionManager.initialize()

# 3. Synchronize Data (Bootstrap)
if not SessionManager.get(SessionManager.DATA, "last_sync"):
    with st.spinner("Synchronizing Research Intelligence..."):
        mongo = MongoService()
        papers = mongo.get_all_papers()
        search_engine = SearchService(papers, {}) # Abbr map built on fly
        abbr_map = search_engine.build_abbreviation_map(papers)
        
        SessionManager.update(SessionManager.DATA, {
            "papers": papers,
            "abbr_map": abbr_map,
            "stats": mongo.get_stats(),
            "last_sync": time.time() if 'time' in globals() else 1
        })

# 4. Navigation Definition
pages = {
    "Discovery": [
        st.Page("pages/home.py", title="Home", icon="🏠", default=True),
        st.Page("pages/search.py", title="Search", icon="🔍"),
        st.Page("pages/explore.py", title="Explore", icon="🧭"),
        st.Page("pages/trending.py", title="Trending", icon="🔥")
    ],
    "Intelligence": [
        st.Page("pages/dashboard.py", title="Dashboard", icon="📊"),
        st.Page("pages/analytics.py", title="Analytics", icon="📈")
    ],
    "Library": [
        st.Page("pages/saved_papers.py", title="Bookmarks", icon="🔖"),
        st.Page("pages/notes.py", title="My Notes", icon="📝")
    ],
    "System": [
        st.Page("pages/settings.py", title="Settings", icon="⚙️")
    ]
}

# Handle Paper Details View (Modal-like overlay or dedicated route)
if st.session_state.get("selected_paper"):
    details_page = st.Page("pages/paper_details.py", title="Paper Analysis", icon="📄")
    # Prepend to nav if active
    pg = st.navigation([details_page] + pages["Discovery"] + pages["Intelligence"], position="sidebar")
else:
    pg = st.navigation(pages)

# 5. Global Sidebar Layout
from components.command_palette import render_command_palette

with st.sidebar:
    st.markdown(f"""
        <div style='display: flex; align-items: center; gap: 12px; padding: 20px 0;'>
            <div style='width: 40px; height: 40px; background: linear-gradient(135deg, {THEME["primary_accent"]}, {THEME["secondary_accent"]}); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 900; font-size: 1.5rem; box-shadow: {THEME["glow_primary"]};'>A</div>
            <div>
                <h1 style='color: white; margin: 0; font-size: 1.4rem; letter-spacing: -1px;'>AETHER</h1>
                <p style='color: {THEME["text_muted"]}; font-size: 0.65rem; font-weight: 700; margin: 0; text-transform: uppercase;'>Research Intelligence</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    render_command_palette()
    
    st.divider()
    
    # Simple User Profile Placeholder
    st.markdown(f"""
        <div style='display: flex; align-items: center; gap: 12px; padding: 10px; background: {THEME["secondary"]}; border-radius: 12px; border: 1px solid {THEME["border"]};'>
            <div style='width: 32px; height: 32px; border-radius: 50%; background: linear-gradient(135deg, {THEME["primary_accent"]}, {THEME["secondary_accent"]});'></div>
            <div>
                <p style='margin: 0; font-size: 0.85rem; font-weight: 700;'>Researcher</p>
                <p style='margin: 0; font-size: 0.7rem; color: {THEME["text_muted"]};'>Pro Plan</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# 6. Execution
pg.run()

# 7. Global Notifications & Toasts (Managed by state)
toasts = SessionManager.get(SessionManager.UI, "toasts")
if toasts:
    for toast in toasts:
        st.toast(toast['message'], icon=toast.get('icon', '🔔'))
    SessionManager.set(SessionManager.UI, "toasts", [])
