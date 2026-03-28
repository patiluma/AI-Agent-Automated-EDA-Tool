import streamlit as st
import pandas as pd
from agent import get_agent

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Agent - Automated EDA Tool",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: #0a0a0f;
    color: #e8e8f0;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem 3rem; max-width: 1100px; }

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #0d0d1a 0%, #0a1628 50%, #0d0d1a 100%);
    border: 1px solid #1e2d4a;
    border-radius: 20px;
    padding: 3rem 3.5rem;
    margin-bottom: 2.5rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(99,179,237,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.hero-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    color: #63b3ed;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}
.hero h1 {
    font-size: 3rem;
    font-weight: 800;
    line-height: 1.1;
    margin: 0 0 1rem 0;
    background: linear-gradient(135deg, #e8e8f0 30%, #63b3ed 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero p {
    color: #8892a4;
    font-size: 1.05rem;
    font-weight: 400;
    max-width: 520px;
    line-height: 1.6;
    margin: 0;
}

/* ── Stat cards ── */
.stats-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
}
.stat-card {
    flex: 1;
    background: #0d1117;
    border: 1px solid #1e2d4a;
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    text-align: center;
}
.stat-number {
    font-size: 1.8rem;
    font-weight: 800;
    color: #63b3ed;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.stat-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    color: #4a5568;
    text-transform: uppercase;
}

/* ── Section headers ── */
.section-header {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    color: #63b3ed;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
    margin-top: 2rem;
}

/* ── Upload area ── */
[data-testid="stFileUploader"] {
    background: #0d1117 !important;
    border: 1.5px dashed #1e2d4a !important;
    border-radius: 14px !important;
    padding: 1.5rem !important;
    transition: border-color 0.2s;
}
[data-testid="stFileUploader"]:hover {
    border-color: #63b3ed !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid #1e2d4a;
    border-radius: 12px;
    overflow: hidden;
}

/* ── Input box ── */
[data-testid="stTextInput"] input {
    background: #0d1117 !important;
    border: 1.5px solid #1e2d4a !important;
    border-radius: 10px !important;
    color: #e8e8f0 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s;
}
[data-testid="stTextInput"] input:focus {
    border-color: #63b3ed !important;
    box-shadow: 0 0 0 3px rgba(99,179,237,0.08) !important;
}

/* ── Button ── */
[data-testid="stButton"] button {
    background: linear-gradient(135deg, #2b6cb0, #3182ce) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.05em !important;
    padding: 0.65rem 2rem !important;
    transition: all 0.2s !important;
}
[data-testid="stButton"] button:hover {
    background: linear-gradient(135deg, #3182ce, #4299e1) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(99,179,237,0.25) !important;
}

/* ── Answer card ── */
.answer-card {
    background: linear-gradient(135deg, #0d1117 0%, #0a1628 100%);
    border: 1px solid #1e3a5f;
    border-left: 3px solid #63b3ed;
    border-radius: 14px;
    padding: 1.5rem 2rem;
    margin-top: 1.5rem;
    font-size: 1rem;
    line-height: 1.7;
    color: #c8d6e5;
}
.answer-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    color: #63b3ed;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0d1117 !important;
    border-right: 1px solid #1e2d4a !important;
}
[data-testid="stSidebar"] .block-container {
    padding: 2rem 1.5rem;
}

/* ── Sidebar chips ── */
.chip {
    background: #0a1628;
    border: 1px solid #1e3a5f;
    border-radius: 8px;
    padding: 0.6rem 0.9rem;
    margin-bottom: 0.5rem;
    font-size: 0.82rem;
    color: #8892a4;
    cursor: pointer;
    transition: all 0.15s;
    font-family: 'DM Mono', monospace;
}
.chip:hover {
    border-color: #63b3ed;
    color: #63b3ed;
    background: #0a1628;
}

/* ── History item ── */
.history-item {
    background: #0d1117;
    border: 1px solid #1e2d4a;
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.75rem;
}
.history-q {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    color: #63b3ed;
    margin-bottom: 0.4rem;
}
.history-a {
    font-size: 0.85rem;
    color: #8892a4;
    line-height: 1.5;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='margin-bottom:1.5rem'>
        <div style='font-size:1.3rem;font-weight:800;color:#e8e8f0'>
            Automated EDA Tool
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='font-family:DM Mono,monospace;font-size:0.65rem;letter-spacing:0.15em;
                color:#4a5568;text-transform:uppercase;margin-bottom:0.75rem'>
        💡 Sample Questions
    </div>
    """, unsafe_allow_html=True)

    sample_questions = [
        "Which age group spends the most?",
        "Average purchase by gender?",
        "Top 5 most purchased products?",
        "Which city has highest sales?",
        "How many unique users?",
        "What is the total revenue?",
    ]
    for q in sample_questions:
        st.markdown(f"<div class='chip'>→ {q}</div>", unsafe_allow_html=True)

    if st.session_state.history:
        st.markdown("""
        <div style='font-family:DM Mono,monospace;font-size:0.65rem;letter-spacing:0.15em;
                    color:#4a5568;text-transform:uppercase;margin:1.5rem 0 0.75rem 0'>
            📋 History
        </div>
        """, unsafe_allow_html=True)
        for item in reversed(st.session_state.history[-4:]):
            st.markdown(f"""
            <div class='history-item'>
                <div class='history-q'>Q: {item['q'][:45]}{'...' if len(item['q'])>45 else ''}</div>
                <div class='history-a'>{item['a'][:120]}{'...' if len(item['a'])>120 else ''}</div>
            </div>
            """, unsafe_allow_html=True)

# ── Main content ───────────────────────────────────────────────────────────────
st.markdown("""
<div class='hero'>
    <div class='hero-label'>🧠 Agentic AI — LangChain + Groq</div>
    <h1>Chat with<br/>your Data</h1>
    <p>Upload any CSV and ask questions in plain English.</p>
</div>
""", unsafe_allow_html=True)

# ── Upload ─────────────────────────────────────────────────────────────────────
st.markdown("<div class='section-header'>📂 Upload Dataset</div>", unsafe_allow_html=True)
file = st.file_uploader("", type=["csv"], label_visibility="collapsed")

if file:
    df = pd.read_csv(file)

    # Stats row
    st.markdown(f"""
    <div class='stats-row'>
        <div class='stat-card'>
            <div class='stat-number'>{df.shape[0]:,}</div>
            <div class='stat-label'>Rows</div>
        </div>
        <div class='stat-card'>
            <div class='stat-number'>{df.shape[1]}</div>
            <div class='stat-label'>Columns</div>
        </div>
        <div class='stat-card'>
            <div class='stat-number'>{df.isnull().sum().sum()}</div>
            <div class='stat-label'>Missing Values</div>
        </div>
        <div class='stat-card'>
            <div class='stat-number'>{df.select_dtypes(include='number').shape[1]}</div>
            <div class='stat-label'>Numeric Cols</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Preview
    st.markdown("<div class='section-header'>👁 Data Preview</div>", unsafe_allow_html=True)
    st.dataframe(df.head(8), use_container_width=True)

    # Ask
    st.markdown("<div class='section-header'>💬 Ask the Agent</div>", unsafe_allow_html=True)
    col1, col2 = st.columns([5, 1])
    with col1:
        question = st.text_input("", placeholder="e.g. Which age group has the highest average purchase?", label_visibility="collapsed")
    with col2:
        analyze = st.button("Analyze →")

    if analyze and question:
        with st.spinner("Agent is reasoning..."):
            try:
                agent = get_agent(df)
                result = agent.invoke(question)
                answer = result["output"]

                st.markdown(f"""
                <div class='answer-card'>
                    <div class='answer-label'>Agent Response</div>
                    {answer}
                </div>
                """, unsafe_allow_html=True)

                # Save to history
                st.session_state.history.append({"q": question, "a": answer})

            except Exception as e:
                st.error(f"Something went wrong: {e}")

    elif analyze and not question:
        st.warning("Please type a question first!")

else:
    # Empty state
    st.markdown("""
    <div style='text-align:center;padding:4rem 2rem;border:1.5px dashed #1e2d4a;
                border-radius:20px;margin-top:1rem'>
        <div style='font-size:3rem;margin-bottom:1rem'>📊</div>
        <div style='font-size:1.1rem;font-weight:700;color:#e8e8f0;margin-bottom:0.5rem'>
            No dataset loaded
        </div>
        <div style='font-size:0.9rem;color:#4a5568'>
            Upload a CSV file above to get started
        </div>
    </div>
    """, unsafe_allow_html=True)
