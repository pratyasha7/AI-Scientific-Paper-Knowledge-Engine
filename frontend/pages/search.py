import streamlit as st
from config import THEME
from state.session_manager import SessionManager
from services.search_service import SearchService
from components.paper_card import render_paper_card

def render_search():
    st.write("# Discover Research")
    
    # 1. Search Bar Logic (Wrapped in High-Contrast Panel)
    st.markdown("<div class='data-panel'>", unsafe_allow_html=True)
    search_state = SessionManager.get(SessionManager.SEARCH)
    query = st.text_input(
        "Search papers, topics, or authors...", 
        value=search_state["query"],
        placeholder="e.g. Generative AI, Quantum Computing...",
        label_visibility="collapsed"
    )
    
    # 2. Advanced Filters (Horizontal)
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
    with col1:
        sort_by = st.selectbox("Sort Order", ["Relevance", "Newest", "Oldest"])
    with col2:
        st.multiselect("Topics", ["Machine Learning", "Physics", "BioTech", "AI Ethics"])
    with col3:
        relevance_min = st.slider("Min Relevance", 0, 100, search_state["filters"]["relevance"])
    with col4:
        st.write("##")
        if st.button("Reset", use_container_width=True):
            SessionManager.set(SessionManager.SEARCH, "query", "")
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # 3. Execution Logic
    if query:
        SessionManager.set(SessionManager.SEARCH, "query", query)
        
        # Service Initialization
        data = SessionManager.get(SessionManager.DATA)
        search_engine = SearchService(data["papers"], data["abbr_map"])
        
        # Acronym Expansion Check
        upper_query = query.upper()
        expanded = []
        if upper_query in data["abbr_map"]:
            options = list(data["abbr_map"][upper_query])
            st.info(f"Detected Acronym: {upper_query}")
            selected_expansion = st.radio("Refine Search Context:", options + ["General Search"], horizontal=True)
            if selected_expansion != "General Search":
                expanded = [upper_query]
                query = selected_expansion

        # Execute Search
        from components.skeleton import render_paper_skeleton
        
        with st.status("Scanning Research Knowledge Graph...", expanded=False) as status:
            # Show skeletons while processing
            skeleton_placeholder = st.empty()
            with skeleton_placeholder.container():
                for _ in range(3):
                    render_paper_skeleton()
            
            results = search_engine.search(query, expanded_terms=expanded)
            
            # Clear skeletons
            skeleton_placeholder.empty()
            status.update(label=f"Analysis Complete: {len(results)} matches found.", state="complete")

        # 4. Results Rendering
        if results:
            # Simple Pagination logic (Top 20)
            for i, res in enumerate(results[:20]):
                render_paper_card(res['data'], score=res['score'], key=f"search_{i}")
        else:
            st.markdown(f"""
                <div style='text-align: center; padding: 100px 0;'>
                    <div style='font-size: 4rem; color: {THEME["text_muted"]}; margin-bottom: 20px;'>🔍</div>
                    <h3>No exact matches found</h3>
                    <p style='color: {THEME["text_muted"]};'>Try broadening your search terms or adjusting the relevance filter.</p>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    render_search()
