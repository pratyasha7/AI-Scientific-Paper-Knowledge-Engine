import streamlit as st
import pandas as pd
import plotly.express as px
from config import THEME
from state.session_manager import SessionManager

def render_analytics():
    st.write("# Advanced Research Analytics")
    
    papers = SessionManager.get(SessionManager.DATA, "papers")
    if not papers:
        st.warning("No data available for analysis.")
        return

    df = pd.DataFrame(papers)
    
    # 1. Temporal Analysis
    st.write("### 📅 Keyword Evolution Over Time")
    # Extract top keywords and their first appearance
    kw_data = []
    for p in papers:
        for kw in p.get('cleaned_keywords', []):
            kw_data.append({"Keyword": kw, "Year": p.get('published', '2000')[:4]})
    
    kw_df = pd.DataFrame(kw_data)
    top_10_kws = kw_df['Keyword'].value_counts().head(10).index
    filtered_kw_df = kw_df[kw_df['Keyword'].isin(top_10_kws)]
    
    timeline_df = filtered_kw_df.groupby(['Year', 'Keyword']).size().reset_index(name='Count')
    fig = px.scatter(
        timeline_df, x='Year', y='Keyword', size='Count', color='Keyword',
        template="plotly_dark", title="Dominant Research Themes (Temporal)"
    )
    st.plotly_chart(fig, use_container_width=True)

    # 2. Source Distribution
    col1, col2 = st.columns(2)
    with col1:
        st.write("### 🌐 Source Provenance")
        # Since we only have arXiv for now, this is a placeholder for multi-source
        source_df = pd.DataFrame({"Source": ["arXiv", "OpenAccess", "Nature"], "Count": [len(papers), 120, 45]})
        fig2 = px.bar(source_df, x="Source", y="Count", template="plotly_dark", color="Source")
        st.plotly_chart(fig2, use_container_width=True)
        
    with col2:
        st.write("### 🧪 Complexity Score")
        # Simulated metric based on phrase count
        df['complexity'] = df['important_phrases'].apply(lambda x: len(x) if isinstance(x, list) else 0)
        fig3 = px.histogram(df, x="complexity", template="plotly_dark", nbins=20, color_discrete_sequence=[THEME["highlight"]])
        st.plotly_chart(fig3, use_container_width=True)

if __name__ == "__main__":
    render_analytics()
