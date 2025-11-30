"""
PRIME - Enterprise Edition
Strict enterprise SaaS aesthetic with minimal flat design.
"""
import shutil, os
from prime_agent.config import CHROMA_PATH

# 🔥 TEMP FIX: Delete corrupted Chroma folder automatically
if os.path.exists(CHROMA_PATH):
    shutil.rmtree(CHROMA_PATH)
    print("🔥 Deleted corrupted chroma_db folder")


import streamlit as st
if os.path.exists("cleanup_chroma.py"):
    import cleanup_chroma
import sys
import pysqlite3 # <--- NEW: Required for SQLite fix
from pathlib import Path
try:
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    # If pysqlite3 is not available (e.g., local test), ignore the swap.
    pass 
# -----------------------------------------------------

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
# --- HOTFIX START ---
import google.generativeai as genai
try:
    # Fix 1: MediaResolution
    if not hasattr(genai.GenerationConfig, "MediaResolution"):
        class FakeMediaResolution:
            AUTO = "auto"
            LOW = "low"
            MEDIUM = "medium"
            HIGH = "high"
        genai.GenerationConfig.MediaResolution = FakeMediaResolution
        
    # Fix 2: Model iteration error (unexpected keyword 'thinking')
    # We need to patch the Model constructor to accept arbitrary kwargs or specifically 'thinking'
    if hasattr(genai.types, "Model"):
        original_init = genai.types.Model.__init__
        def new_init(self, **kwargs):
            # Remove 'thinking' if present, as the current library version doesn't support it
            kwargs.pop('thinking', None)
            original_init(self, **kwargs)
        genai.types.Model.__init__ = new_init
        
except Exception as e:
    print(f"Hotfix warning: {e}")
# --- HOTFIX END ---

from prime_agent.agents.graph_definition import build_graph
from prime_agent.ui.components import (
    render_notes, render_quiz,
    render_flashcards, render_graph, render_sources,
    render_mind_map
)
from prime_agent.tools.user_profile import get_session_history
from prime_agent.logging_config import setup_logging
from prime_agent.tools.list_models import list_and_log_models

setup_logging()
list_and_log_models()

st.set_page_config(
    page_title="PRIME Workspace",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="auto"
)

# ============================================================================
# INJECT MATERIAL SYMBOLS ROUNDED FONT
# ============================================================================

st.markdown("""
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded" />

<style>
.icon {
    font-family: 'Material Symbols Rounded';
    font-size: 28px;
    color: white;
    cursor: pointer;
    vertical-align: middle;
    font-variation-settings:
        'FILL' 0,
        'wght' 400,
        'GRAD' 0,
        'opsz' 48;
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# ENTERPRISE CSS THEME
# ============================================================================

ENTERPRISE_CSS = """
<style>
    /* Import Inter Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    /* CSS Variables - Enterprise System */
    :root {
        --bg-app: #141618;
        --bg-sidebar: #111315;
        --bg-surface: #1F2124;
        --bg-input: #1A1C1F;
        --border-card: #2A2D31;
        --border-input: #373A3F;
        
        --primary-blue: #3A7BFA;
        --primary-hover: #2A6BEA;
        
        --text-primary: #FFFFFF;
        --text-light: #E4E7EC;
        --text-placeholder: #A3A8B0;
        
        --shadow-card: 0 2px 8px rgba(0, 0, 0, 0.18);
    }
    
    /* Base Reset */
    .stApp {
        background-color: var(--bg-app);
        font-family: 'Inter', sans-serif !important;
        color: var(--text-primary);
    }
    
    /* Typography */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600;
        color: var(--text-primary);
        letter-spacing: -0.01em;
    }
    
    p, label, div, span {
        font-family: 'Inter', sans-serif !important;
        color: var(--text-light);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: var(--bg-sidebar) !important;
        border-right: 1px solid var(--border-card);
    }
    
    [data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
    }
    
    /* Inputs */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: var(--bg-input) !important;
        border: 1px solid var(--border-input) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
        padding: 12px 14px !important;
        font-size: 14px !important;
        transition: border-color 0.2s ease;
    }
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: var(--text-placeholder) !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-blue) !important;
        outline: none !important;
        box-shadow: none !important;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: var(--primary-blue) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 14px 28px !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        height: 48px !important;
        transition: background-color 0.2s ease !important;
    }
    
    .stButton > button:hover {
        background-color: var(--primary-hover) !important;
    }
    
    /* Slider */
    .stSlider > div > div > div > div {
        background-color: #E4E7EC !important;
        height: 4px !important;
    }
    
    .stSlider > div > div > div > div > div {
        background-color: var(--primary-blue) !important;
    }
    
    /* Slider Handle - Round Red Button */
    .stSlider > div > div > div > div > div > div {
        background-color: #E74C3C !important;
        border: 2px solid white !important;
        box-shadow: 0 2px 6px rgba(231, 76, 60, 0.4) !important;
        height: 20px !important;
        width: 20px !important;
        border-radius: 50% !important;
        top: -8px !important;
    }
    
    /* Slider Values */
    .stSlider [data-testid="stTickBar"] {
        display: block !important;
    }
    .stSlider [data-testid="stTickBar"] > div {
        color: #E4E7EC !important;
        font-size: 12px !important;
        font-weight: 500 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: var(--bg-surface);
        border-radius: 10px;
        padding: 6px;
        border: 1px solid var(--border-card);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none;
        color: var(--text-placeholder);
        font-weight: 500;
        padding: 10px 20px;
        border-radius: 6px;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(255,255,255,0.05);
        color: var(--text-light);
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: var(--primary-blue);
        color: white;
    }
    
    /* Metrics */
    [data-testid="stMetric"] {
        background-color: var(--bg-surface);
        border: 1px solid var(--border-card);
        border-radius: 10px;
        padding: 20px !important;
        box-shadow: var(--shadow-card);
    }
    
    [data-testid="stMetric"] label {
        color: var(--text-placeholder) !important;
        font-size: 13px !important;
        font-weight: 500;
    }
    
    [data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: var(--text-primary) !important;
        font-size: 24px !important;
        font-weight: 600 !important;
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background-color: var(--bg-surface);
        border: 1px solid var(--border-card);
        border-radius: 10px;
        padding: 28px;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background-color: var(--primary-blue) !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: var(--bg-surface) !important;
        border: 1px solid var(--border-card) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-sidebar);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border-card);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--border-input);
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Hide Deploy button */
    .stAppDeployButton {
        display: none !important;
    }
    
    /* Fix Sidebar Toggle Button */
    [data-testid="collapsedControl"] {
        z-index: 100000 !important;
        color: transparent !important;
    }
    
    /* Hide the text content specifically */
    [data-testid="collapsedControl"] p, 
    [data-testid="collapsedControl"] span {
        display: none !important;
    }
    
    /* Add replacement icon - Simple emoji approach */
    [data-testid="collapsedControl"]::after {
        content: "⏩";
        font-size: 28px;
        color: white;
        cursor: pointer;
        position: absolute;
        left: 20px;
        top: 20px;
    }
    
    /* Slider Values - Force Visible */
    .stSlider [data-testid="stTickBar"] {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        height: auto !important;
    }
    
    .stSlider [data-testid="stTickBar"] > div {
        color: #E4E7EC !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        opacity: 1 !important;
        visibility: visible !important;
        padding-top: 10px !important;
    }
    
    /* Ensure Header Actions are visible (but hide the broken ones if needed) */
    [data-testid="stHeaderActionElements"] {
        display: block !important;
    }
    
</style>
"""

st.markdown(ENTERPRISE_CSS, unsafe_allow_html=True)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # --- TEMPORARY FIX: NUKE THE DATABASE (RUN ONCE) ---
    # Run this ONCE to clear the corrupted folder on the cloud server.
    if os.path.exists("./chroma_db"):
        try:
            shutil.rmtree("./chroma_db")
            print("🗑️ DELETED CORRUPTED DATABASE")
        except Exception as e:
            # If deletion fails, it will still try to run, but print a warning.
            print(f"⚠️ Could not delete database: {e}")
    # ----------------------------------------
    # Sidebar
    with st.sidebar:
        st.markdown("""
            <div style='padding: 16px 0; margin-bottom: 24px; border-bottom: 1px solid #2A2D31;'>
                <div style='display: flex; align-items: center; gap: 12px;'>
                    <div style='width: 36px; height: 36px; background-color: #3A7BFA; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 600; font-size: 16px;'>P</div>
                    <div>
                        <h2 style='font-size: 15px; font-weight: 600; color: white; margin: 0;'>PRIME</h2>
                        <p style='font-size: 12px; color: #A3A8B0; margin: 0;'>Workspace</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<p style='font-size: 11px; font-weight: 600; color: #A3A8B0; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 12px;'>Recent Projects</p>", unsafe_allow_html=True)
        
        history = get_session_history()
        if history:
            for sess in history[:5]:
                st.markdown(f"""
                    <div style='padding: 10px 12px; border-radius: 6px; margin-bottom: 6px; cursor: pointer; color: #E4E7EC; font-size: 13px; background-color: transparent; border: 1px solid transparent; transition: all 0.2s;' onmouseover="this.style.backgroundColor='#1F2124'; this.style.borderColor='#2A2D31'" onmouseout="this.style.backgroundColor='transparent'; this.style.borderColor='transparent'">
                        📄 {sess[1][:18]}...
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("<p style='font-size: 12px; color: #6F737A; opacity: 0.6;'>No recent projects</p>", unsafe_allow_html=True)

    # Header
    st.markdown("""
        <div style='text-align: center; margin-bottom: 32px; margin-top: -20px;'>
            <h1 style='font-size: 32px; font-weight: 600; margin-bottom: 8px; color: #FFFFFF;'>Create New Project</h1>
            <p style='font-size: 14px; color: #A3A8B0;'>Configure your research parameters and start exploring</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Main Grid
    col1, col2 = st.columns([1.2, 0.8], gap="medium")
    
    with col1:
        st.markdown("""
            <div style='background-color: #1F2124; border: 1px solid #2A2D31; border-radius: 10px; padding: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.18);'>
                <h3 style='margin-top: 0; font-size: 16px; margin-bottom: 20px; font-weight: 600; color: #FFFFFF;'>Project Details</h3>
        """, unsafe_allow_html=True)
        
        topic = st.text_input("Research Topic", placeholder="e.g., Impact of AI on Healthcare")
        st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)
        urls_input = st.text_area("Source URLs", placeholder="Paste URLs (one per line)", height=120)
        urls = [u.strip() for u in urls_input.split("\n") if u.strip()]
        
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
            <div style='background-color: #1F2124; border: 1px solid #2A2D31; border-radius: 10px; padding: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.18);'>
                <h3 style='margin-top: 0; font-size: 16px; margin-bottom: 20px; font-weight: 600; color: #FFFFFF;'>Configuration</h3>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin-bottom: 8px;'><label style='font-weight: 500; font-size: 13px; color: #E4E7EC;'>Research Depth</label></div>", unsafe_allow_html=True)
        depth = st.slider("Depth", 1, 5, 2, label_visibility="collapsed")
        
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        uploaded_files = st.file_uploader("Upload Documents", type=["pdf"], accept_multiple_files=True)
        
        pdf_paths = []
        if uploaded_files:
            temp_dir = Path("temp_uploads")
            temp_dir.mkdir(exist_ok=True)
            for uploaded_file in uploaded_files:
                path = temp_dir / uploaded_file.name
                with open(path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                pdf_paths.append(str(path))
                
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 32px;'></div>", unsafe_allow_html=True)
    
    col_btn_l, col_btn_c, col_btn_r = st.columns([1, 1.5, 1])
    with col_btn_c:
        run_btn = st.button("Start Research", type="primary", use_container_width=True)

    if run_btn and topic:
        st.markdown("---")
        
        with st.spinner("Processing..."):
            app = build_graph()
            
            initial_state = {
                "topic": topic,
                "depth": depth,
                "urls": urls,
                "pdf_files": pdf_paths,
                "documents": [],
                "summary": "",
                "notes": {},
                "credibility_scores": [],
                "quiz": [],
                "graph_data": {},
                "mind_map": "",
                "messages": []
            }
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            final_state = None
            step_count = 0
            total_steps = 7
            
            for output in app.stream(initial_state):
                for key, value in output.items():
                    step_count += 1
                    progress = min(step_count / total_steps, 1.0)
                    progress_bar.progress(progress)
                    status_text.caption(f"{key}...")
                    final_state = value
            
            progress_bar.progress(1.0)
            status_text.success("Complete!")
            
            st.session_state["result"] = final_state
    
    if "result" in st.session_state:
        result = st.session_state["result"]
        
        st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            "Overview", "Notes", "Quiz", "Flashcards", "Graph", "Mind Map", "Sources"
        ])
        
        with tab1:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Depth", result.get("depth"))
            with col2:
                st.metric("Sources", len(result.get("documents", [])))
            with col3:
                score = sum([s.get('score', 0) for s in result.get('credibility_scores', [])])
                count = max(len(result.get('credibility_scores', [])), 1)
                st.metric("Quality", f"{score/count:.1f}")
                
        with tab2:
            render_notes(result.get("notes", {}))
        with tab3:
            render_quiz(result.get("quiz", []))
        with tab4:
            render_flashcards(result.get("quiz", []))
        with tab5:
            render_graph(result.get("graph_data", {}))
        with tab6:
            render_mind_map(result.get("mind_map", ""))
        with tab7:
            render_sources(result.get("credibility_scores", []))

if __name__ == "__main__":
    main()
