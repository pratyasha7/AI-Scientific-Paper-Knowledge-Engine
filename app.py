import streamlit as st

# -------- PAGE CONFIG --------
st.set_page_config(
    page_title="AI Scientific Paper Knowledge Engine",
    layout="wide"
)

# -------- HEADER --------
st.title("📚 AI Scientific Paper Knowledge Engine")

st.write("""
Explore, search, and discover scientific research papers using AI-powered search 
built on top of the arXiv research database.
""")

# -------- SEARCH BAR --------
st.markdown("---")

query = st.text_input(
    "🔍 Search research papers from arXiv..."
)

# -------- SEARCH RESULT --------
if query:

    st.success(f"Showing results for: {query}")

    # Example result container
    with st.container():

        st.write("## 📄 Attention Is All You Need")

        st.write("""
        **Authors:** Ashish Vaswani et al.
        
        **Published:** 2017
        
        **Category:** Machine Learning / NLP
        """)

        st.write("""
        This paper introduced the Transformer architecture,
        which became the foundation of modern Large Language Models.
        """)

        st.link_button(
            "Read Paper on arXiv",
            "https://arxiv.org"
        )

        st.markdown("---")

# -------- HOME SECTION --------
st.markdown("---")

st.header("🚀 What We Provide")

col1, col2, col3 = st.columns(3)

with col1:
    st.success("🔍 AI-powered paper discovery")

with col2:
    st.success("📅 Paper sorting by dates")

with col3:
    st.success("📈 Trending research tracking")

# -------- WHY BETTER --------
st.markdown("---")

st.header("⭐ Why Our Platform Is Better")

left, right = st.columns(2)

with left:

    st.info("""
    ✔ Faster paper searching
    
    ✔ Beginner-friendly interface
    
    ✔ Organized research workflow
    
    ✔ AI-assisted discovery
    """)

with right:

    st.info("""
    ✔ Powered using arXiv papers
    
    ✔ Clean and distraction-free UI
    
    ✔ Smart research exploration
    
    ✔ Quick access to trending topics
    """)

# -------- FEATURES --------
st.markdown("---")

st.header("✨ Core Features")

f1, f2, f3 = st.columns(3)

with f1:

    st.write("### 🔎 Smart Search")

    st.write("""
    Search scientific papers instantly 
    using intelligent keyword matching.
    """)

with f2:

    st.write("### 📅 Date-wise Sorting")

    st.write("""
    Organize and explore papers 
    based on publication dates.
    """)

with f3:

    st.write("### 📚 arXiv Integration")

    st.write("""
    Access research papers directly 
    from the arXiv database.
    """)

# -------- TRENDING SECTION --------
st.markdown("---")

st.header("🔥 Trending Research Topics")

t1, t2, t3 = st.columns(3)

with t1:
    st.warning("🧠 Large Language Models")

with t2:
    st.warning("🤖 Generative AI")

with t3:
    st.warning("📷 Computer Vision")

# -------- FOOTER --------
st.markdown("---")

st.caption("Built using Streamlit + arXiv + AI")