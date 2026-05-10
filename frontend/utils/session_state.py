import streamlit as st
from services.mongo_service import MongoService
from services.search_service import SearchService

def init_session_state():
    if "initialized" not in st.session_state:
        st.session_state.mongo_service = MongoService()
        st.session_state.search_service = SearchService()
        st.session_state.papers = st.session_state.mongo_service.get_all_papers()
        st.session_state.abbr_map = st.session_state.search_service.build_abbreviation_map(st.session_state.papers)
        st.session_state.current_query = ""
        st.session_state.search_results = []
        st.session_state.saved_papers = []
        st.session_state.theme = "dark"
        st.session_state.initialized = True

def get_service(service_name):
    return st.session_state.get(service_name)
