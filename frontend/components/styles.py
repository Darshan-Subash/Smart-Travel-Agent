import streamlit as st


def inject_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');

    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

    .stApp { background: #0d1117; color: #e6edf3; }

    [data-testid="stSidebar"] {
        background: #161b22;
        border-right: 1px solid #21262d;
    }

    /* Hero */
    .hero { text-align: center; padding: 3rem 1rem 2rem; }
    .hero h1 {
        font-family: 'Playfair Display', serif;
        font-size: 3.2rem;
        font-weight: 700;
        color: #e6edf3;
        margin-bottom: 0.3rem;
    }
    .hero h1 span { color: #f0a500; }
    .hero p { color: #8b949e; font-size: 1.05rem; font-weight: 300; margin-top: 0; }

    /* Card */
    .card {
        background: #161b22;
        border: 1px solid #21262d;
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
    }
    .card h4 {
        font-family: 'Playfair Display', serif;
        color: #f0a500;
        margin: 0 0 0.5rem 0;
        font-size: 1rem;
    }
    .card p { color: #8b949e; margin: 0; font-size: 0.88rem; line-height: 1.6; }

    /* Agent row */
    .agent-row {
        display: flex;
        align-items: center;
        gap: 0.7rem;
        padding: 0.6rem 0;
        border-bottom: 1px solid #21262d;
        font-size: 0.9rem;
    }
    .agent-row:last-child { border-bottom: none; }
    .agent-name { color: #c9d1d9; flex: 1; }
    .badge { padding: 0.2rem 0.7rem; border-radius: 20px; font-size: 0.75rem; font-weight: 500; }
    .badge-waiting { background: #21262d; color: #8b949e; }
    .badge-running { background: #1f3a1f; color: #3fb950; }
    .badge-done    { background: #162032; color: #58a6ff; }

    /* Result */
    .result-box {
        background: #161b22;
        border: 1px solid #21262d;
        border-left: 4px solid #f0a500;
        border-radius: 0 12px 12px 0;
        padding: 1.8rem 2rem;
        margin-top: 1rem;
        line-height: 1.8;
        color: #c9d1d9;
        font-size: 0.95rem;
        white-space: pre-wrap;
    }

    /* Stats */
    .stat-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; }
    .stat-box {
        flex: 1;
        background: #161b22;
        border: 1px solid #21262d;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .stat-box .val { font-family: 'Playfair Display', serif; font-size: 1.6rem; color: #f0a500; }
    .stat-box .lbl { font-size: 0.78rem; color: #8b949e; margin-top: 0.1rem; }

    /* Inputs */
    .stTextInput input, .stNumberInput input, .stDateInput input {
        background: #21262d !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
        color: #e6edf3 !important;
    }
    .stTextInput input:focus {
        border-color: #f0a500 !important;
        box-shadow: 0 0 0 3px rgba(240,165,0,0.15) !important;
    }

    /* Button */
    .stButton > button {
        background: linear-gradient(135deg, #f0a500, #e07b00) !important;
        color: #0d1117 !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        padding: 0.65rem 2rem !important;
        width: 100% !important;
        transition: opacity 0.2s !important;
    }
    .stButton > button:hover { opacity: 0.88 !important; }

    hr { border-color: #21262d !important; }
    .stSpinner > div { color: #f0a500 !important; }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: #161b22;
        border-radius: 8px;
        padding: 0.2rem;
        gap: 0.2rem;
    }
    .stTabs [data-baseweb="tab"] {
        color: #8b949e !important;
        border-radius: 6px !important;
        font-size: 0.88rem !important;
    }
    .stTabs [aria-selected="true"] {
        background: #21262d !important;
        color: #f0a500 !important;
    }
    </style>
    """, unsafe_allow_html=True)
