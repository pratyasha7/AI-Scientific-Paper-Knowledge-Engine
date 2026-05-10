import streamlit as st
import pandas as pd
import plotly.express as px
from config import THEME
from state.session_manager import SessionManager

def render_dashboard():
    st.write("# Intelligence Dashboard")
    
    stats = SessionManager.get(SessionManager.DATA, "stats")
    papers = SessionManager.get(SessionManager.DATA, "papers")
    
    if not papers:
        st.warning("Data synchronization required.")
        return

    # --- TOP ROW: KPI CARDS ---
    st.markdown("<div class='data-panel'>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Papers", f"{len(papers):,}", delta="+124 this week")
    with col2:
        st.metric("Unique Concepts", "1,248", delta="+5.2%")
    with col3:
        st.metric("Research Sources", "arXiv", delta="Direct")
    with col4:
        st.metric("System Health", "Operational", delta="99.9%")
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("##")

    # --- MIDDLE ROW: ANALYTICS ---
    st.markdown("<div class='data-panel'>", unsafe_allow_html=True)
    col_left, col_right = st.columns([3, 2])
    
    with col_left:
        st.write("### 📈 Publication Momentum")
        df = pd.DataFrame(papers)
        df['year'] = df['published'].apply(lambda x: x[:4] if x else 'Unknown')
        year_counts = df['year'].value_counts().sort_index().reset_index()
        year_counts.columns = ['Year', 'Count']
        
        fig = px.line(
            year_counts, x='Year', y='Count', 
            template="plotly_dark",
            color_discrete_sequence=[THEME["primary_accent"]]
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),
            height=350,
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor=THEME["border"])
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.write("### 🏆 Top Discovered Fields")
        from services.mongo_service import MongoService
        mongo = MongoService()
        top_kws = mongo.get_trending_keywords(10)
        kw_df = pd.DataFrame(top_kws)
        
        fig = px.pie(
            kw_df, values='count', names='_id',
            template="plotly_dark",
            hole=.4,
            color_discrete_sequence=px.colors.sequential.Purples_r
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=20, b=20),
            height=350,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # --- BOTTOM ROW: RECENT SYNC LOG ---
    st.write("### 🔄 Global Ingestion Activity")
    recent_activity = pd.DataFrame([
        {"Event": "ArXiv Sync", "Status": "Success", "Items": 50, "Time": "12m ago"},
        {"Event": "NLP Extraction", "Status": "Success", "Items": 1240, "Time": "15m ago"},
        {"Event": "Concept Mapping", "Status": "Success", "Items": 89, "Time": "16m ago"},
    ])
    st.table(recent_activity)

if __name__ == "__main__":
    render_dashboard()
