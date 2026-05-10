import streamlit as st
from typing import Any, Dict

class SessionManager:
    """
    Centralized manager for st.session_state with namespacing and persistence.
    """
    
    # Namespaces
    UI = "ui"
    SEARCH = "search"
    USER = "user"
    DATA = "data"
    
    @staticmethod
    def initialize():
        """Initialize all session state namespaces."""
        if "initialized" not in st.session_state:
            # UI State
            st.session_state[SessionManager.UI] = {
                "theme": "dark",
                "sidebar_expanded": True,
                "current_page": "home",
                "toasts": [],
                "notifications": []
            }
            
            # Search State
            st.session_state[SessionManager.SEARCH] = {
                "query": "",
                "results": [],
                "filters": {
                    "date_range": [],
                    "categories": [],
                    "relevance": 10
                },
                "history": [],
                "last_search_time": None
            }
            
            # User State
            st.session_state[SessionManager.USER] = {
                "bookmarks": [],
                "notes": {},
                "preferences": {
                    "compact_mode": False,
                    "font_scale": 1.0
                }
            }
            
            # Data State (Cache for backend responses)
            st.session_state[SessionManager.DATA] = {
                "papers": [],
                "abbr_map": {},
                "stats": {},
                "last_sync": None
            }
            
            st.session_state.initialized = True

    @staticmethod
    def get(namespace: str, key: str = None) -> Any:
        if namespace not in st.session_state:
            return None
        if key:
            return st.session_state[namespace].get(key)
        return st.session_state[namespace]

    @staticmethod
    def set(namespace: str, key: str, value: Any):
        if namespace in st.session_state:
            st.session_state[namespace][key] = value

    @staticmethod
    def update(namespace: str, data: Dict[str, Any]):
        if namespace in st.session_state:
            st.session_state[namespace].update(data)

    @staticmethod
    def add_bookmark(paper: Dict):
        bookmarks = SessionManager.get(SessionManager.USER, "bookmarks")
        if paper not in bookmarks:
            bookmarks.append(paper)
            SessionManager.set(SessionManager.USER, "bookmarks", bookmarks)

    @staticmethod
    def remove_bookmark(paper: Dict):
        bookmarks = SessionManager.get(SessionManager.USER, "bookmarks")
        bookmarks = [b for b in bookmarks if b.get('url') != paper.get('url')]
        SessionManager.set(SessionManager.USER, "bookmarks", bookmarks)
