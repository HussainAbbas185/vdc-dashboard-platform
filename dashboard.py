
import streamlit as st
import os
import time
from src.audit_logger import log_action

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="VDC | MASTER TERMINAL",
    layout="wide",
    page_icon="🏢",
    initial_sidebar_state="expanded"
)

# --- VDC "PREMIUM DAYLIGHT" THEME ---
# High-Visibility Light Mode Aesthetic with Glassmorphism
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap');
    
    :root {
        --bg-core: #f8fafc;
        --bg-panel: #ffffff;
        --text-main: #0f172a;
        --text-sub: #475569;
        --primary: #1e293b;
        --accent: #2563eb;
        --accent-glow: rgba(37, 99, 235, 0.4);
        --border: rgba(0,0,0,0.1);
        --panel-radius: 12px;
    }

    /* GLOBAL RESET */
    .stApp, .stApp > header {
        background-color: var(--bg-core);
        background-image: radial-gradient(circle at 50% 0%, rgba(37, 99, 235, 0.05) 0%, transparent 50%);
        color: var(--text-main);
        font-family: 'Outfit', sans-serif;
    }

    /* HEADERS */
    .vdc-main-header {
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        font-size: 2.8rem;
        background: linear-gradient(90deg, #0f172a, #334155);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.03em;
        margin-bottom: 0.5rem;
        border-bottom: 1px solid var(--border);
        padding-bottom: 1rem;
    }

    h1, h2, h3 {
        font-family: 'Outfit', sans-serif !important;
        color: var(--text-main) !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em !important;
    }

    /* CARDS & PANELS */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--panel-radius) !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 0 15px var(--accent-glow) !important;
        border-color: rgba(37, 99, 235, 0.4) !important;
        transform: translateY(-2px);
    }

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background-color: var(--bg-panel) !important;
        border-right: 1px solid var(--border);
    }
    [data-testid="stSidebarNav"] {
        background-color: transparent !important;
    }

    /* METRICS */
    [data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
        color: var(--text-main) !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        text-shadow: 0 0 10px rgba(0,0,0,0.05);
    }

    [data-testid="stMetricLabel"] {
        color: var(--text-sub) !important;
        font-size: 0.95rem !important;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    [data-testid="stMetricDelta"] {
        font-weight: 600 !important;
    }

    /* BUTTONS */
    .stButton>button {
        background: linear-gradient(180deg, rgba(255, 255, 255, 1) 0%, rgba(248, 250, 252, 1) 100%) !important;
        color: var(--text-main) !important;
        border: 1px solid var(--border) !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.2s ease;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
    }

    .stButton>button:hover {
        border-color: var(--accent) !important;
        color: var(--accent) !important;
        background: linear-gradient(180deg, rgba(239, 246, 255, 0.8) 0%, rgba(219, 234, 254, 0.8) 100%) !important;
        box-shadow: 0 0 10px var(--accent-glow) !important;
        transform: translateY(-1px);
    }
    
    .stButton>button:active {
        transform: translateY(1px);
    }

    /* INPUTS & SELECTS */
    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.9) !important;
        color: var(--text-main) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        font-family: 'Outfit', sans-serif !important;
        transition: all 0.2s;
    }
    
    .stTextInput input:focus, .stSelectbox div[data-baseweb="select"]:focus-within, .stTextArea textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 1px var(--accent) !important;
    }

    /* DATA FRAMES / TABLES */
    [data-testid="stDataFrame"] {
        background-color: rgba(255, 255, 255, 0.7);
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid var(--border);
    }

    /* RADIO BUTTONS (SIDEBAR NAV) */
    div.row-widget.stRadio > div {
        background-color: transparent;
        padding: 0;
        gap: 0.2rem;
    }
    div.row-widget.stRadio > div > label {
        background-color: transparent !important;
        border: none !important;
        padding: 0.4rem 0.8rem !important;
        border-radius: 6px !important;
        transition: all 0.2s !important;
        font-weight: 500 !important;
        color: var(--text-sub) !important;
        cursor: pointer !important;
    }
    div.row-widget.stRadio > div > label:hover {
        background-color: rgba(0,0,0,0.03) !important;
        color: var(--text-main) !important;
    }
    div.row-widget.stRadio > div > label[data-checked="true"],
    div.row-widget.stRadio > div > label[data-checked="true"]:hover {
        background-color: rgba(37, 99, 235, 0.1) !important;
        color: var(--accent) !important;
        border-left: 3px solid var(--accent) !important;
        border-top-left-radius: 0 !important;
        border-bottom-left-radius: 0 !important;
    }

    /* TABS */
    button[data-baseweb="tab"] {
        background-color: transparent !important;
        color: var(--text-sub) !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 500 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: var(--text-main) !important;
        border-bottom-color: var(--accent) !important;
    }

    /* EXPANDERS */
    [data-testid="stExpander"] {
        background-color: rgba(255, 255, 255, 0.6) !important;
        border-radius: 8px !important;
        border: 1px solid var(--border) !important;
    }
    [data-testid="stExpander"] summary {
        font-weight: 600 !important;
        color: var(--text-main) !important;
    }
    [data-testid="stExpander"] summary:hover {
        color: var(--accent) !important;
    }

</style>
""", unsafe_allow_html=True)

# --- SYSTEM INITIALIZATION LOG ---
if 'init_done' not in st.session_state:
    log_action("System", "Initialization", "VDC KERNEL ACTIVE", "CORE", "CRITICAL")
    st.session_state.init_done = True

# --- SIDEBAR HUD ---
with st.sidebar:
    st.markdown("<h1>VDC <span style='font-size:0.6em; color:#64748b'>// PRO</span></h1>", unsafe_allow_html=True)
    st.caption("v4.5.3 | ENTERPRISE EDITION")
    
    # SYSTEM PULSE
    try:
        from src.server_stats import get_system_metrics
        m = get_system_metrics()
        
        st.divider()
        st.caption("INFRASTRUCTURE STATUS")
        c1, c2 = st.columns(2)
        c1.metric("CPU", f"{m['cpu_percent']}%")
        c2.metric("RAM", f"{m['ram_percent']}%")
        st.progress(m['cpu_percent'] / 100)
    except: pass

    st.divider()
    
    # NEURAL COMMAND LINE
    st.markdown("### Command Interface")
    try:
        from src.intelligence_core import IntelligenceCore
        ic = IntelligenceCore()
        u_cmd = st.text_input("Terminal Input", placeholder="Execute neural instruction...", label_visibility="collapsed")
        if u_cmd:
            resp = ic.process_neural_command(u_cmd)
            with st.chat_message("assistant"):
                st.write(resp['message'])
            if resp['action'] == "NAVIGATE":
                if st.button(f"Navigate: {resp['target']}", use_container_width=True):
                    st.session_state.target_page = resp['target']
                    st.rerun()
    except: pass

    st.divider()
    
    # NAV MATRIX
    st.caption("Modules")
    page = st.radio("System Navigation", [
        "Global Command Center",
        "Executive Intelligence Hub",
        "Digital Twin Controller",
        "Quantum Orchestrator",
        "Venture Intelligence",
        "Data Lab & Mining", 
        "Security Audit Ledger",
        "Visualization Studio",
        "Global Tech News",
        "Extraction Engine",
        "Molecular DNA Archival",
        "Real-Time Monitor",
        "Social Market Intelligence",
        "Connect Database",
        "File Utilities",
        "Workflow Automation",
        "Legacy Dashboard"
    ])

# NAV HANDLER
if 'target_page' in st.session_state:
    page = st.session_state.target_page
    del st.session_state.target_page
    
# PAGE AUDIT
if 'last_page' not in st.session_state: st.session_state.last_page = None
if st.session_state.last_page != page:
    log_action("User", "Nav", f"Switched to {page}", "UI", "Low")
    st.session_state.last_page = page

# --- ROUTER DELEGATION ---
if page == "Global Command Center":
    from src.ui.command_center import render_command_center
    render_command_center()

elif page == "Digital Twin Controller":
    from src.ui.advanced_ui import render_digital_twin_controller
    render_digital_twin_controller()

elif page == "Executive Intelligence Hub":
    from src.ui.intelligence import render_executive_intelligence_hub
    render_executive_intelligence_hub()

elif page == "Quantum Orchestrator":
    from src.ui.quantum_ui import render_quantum_orchestrator
    render_quantum_orchestrator()

elif page == "Venture Intelligence":
    from src.ui.intelligence import render_venture_intelligence
    render_venture_intelligence()

elif page == "Data Lab & Mining":
    from src.ui.data_mgmt import render_data_lab_and_mining
    render_data_lab_and_mining()

elif page == "Security Audit Ledger":
    from src.ui.advanced_ui import render_security_audit_ledger
    render_security_audit_ledger()

elif page == "Visualization Studio":
    from src.ui.tools_ui import render_visualization_studio
    render_visualization_studio()

elif page == "Global Tech News":
    from src.ui.tech_news import render_global_tech_news
    render_global_tech_news()

elif page == "Extraction Engine":
    from src.ui.tools_ui import render_extraction_engine
    render_extraction_engine()

elif page == "Molecular DNA Archival":
    from src.ui.advanced_ui import render_molecular_dna_archival
    render_molecular_dna_archival()

elif page == "Social Market Intelligence":
    from src.ui.intelligence import render_social_market_intelligence
    render_social_market_intelligence()

elif page == "Real-Time Monitor":
    from src.ui.data_mgmt import render_real_time_monitor
    render_real_time_monitor()

elif page == "Connect Database":
    from src.ui.data_mgmt import render_connect_database
    render_connect_database()

elif page == "File Utilities":
    from src.ui.tools_ui import render_file_utilities
    render_file_utilities()

elif page == "Workflow Automation":
    from src.ui.tools_ui import render_workflow_automation
    render_workflow_automation()

elif page == "Legacy Dashboard":
    from src.ui.data_mgmt import render_legacy_dashboard
    render_legacy_dashboard()
