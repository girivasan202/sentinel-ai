import streamlit as st
import re
import pandas as pd
from datetime import datetime

# --- 1. CORE SYSTEM CONFIG ---
st.set_page_config(
    page_title="SENTINEL // OVERSEER", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. DEEP NAVY / CYBER-CYAN CSS ENGINE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600;700&family=Inter:wght@400;600;800&display=swap');

    /* Global Base: Deep Navy/Charcoal */
    .stApp {
        background-color: #070B19 !important; /* Deepest Navy Base */
        color: #FFFFFF !important; 
        font-family: 'Inter', sans-serif !important;
    }

    /* Solid Charcoal Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0F1423 !important; /* Charcoal Navy */
        border-right: 1px solid #00E5FF !important; /* Electric Cyan Border */
        min-width: 320px !important;
        max-width: 320px !important;
        transform: none !important;
        left: 0 !important;
    }
    
    [data-testid="stMainView"] { margin-left: 0px !important; }

    /* Headers & Typography */
    h1, h2, h3, h4, h5, label {
        font-family: 'Fira Code', monospace !important;
        color: #00E5FF !important; /* Electric Cyan */
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 700 !important;
    }
    
    .brand-sidebar { 
        color: #00FF66 !important; /* Neon Green Branding */
        font-family: 'Fira Code', monospace;
        font-weight: 800; 
        font-size: 2.2rem; 
        margin-bottom: 20px; 
        text-shadow: 0 0 15px rgba(0, 255, 102, 0.4); 
    }

    /* Tabs Layout */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent !important;
        border-bottom: 1px solid rgba(0, 229, 255, 0.3) !important;
        gap: 0px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #6B7280 !important;
        font-family: 'Fira Code', monospace !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        color: #FFFFFF !important; 
        -webkit-text-fill-color: #FFFFFF !important;
        border-bottom: 3px solid #00E5FF !important; /* Cyan Active Tab */
        background-color: #0F1423 !important;
    }

    /* Bulletproof Input Fields (High Contrast White Text) */
    .stTextInput input, 
    .stTextArea textarea, 
    [data-baseweb="base-input"] input, 
    [data-baseweb="textarea"] textarea,
    textarea, input {
        background-color: #151A2C !important; /* Darker Input Background */
        border: 1px solid #00E5FF !important; /* Cyan Border */
        color: #FFFFFF !important; 
        -webkit-text-fill-color: #FFFFFF !important; 
        font-family: 'Fira Code', monospace !important;
        font-size: 15px !important;
        font-weight: 600 !important; 
        border-radius: 2px !important;
    }
    
    .stTextInput input:focus, 
    .stTextArea textarea:focus {
        border-color: #00FF66 !important; /* Neon Green on Focus */
        box-shadow: 0 0 12px rgba(0, 255, 102, 0.2) !important;
    }

    /* Core Action Buttons */
    .stButton button {
        background-color: #00E5FF !important; /* Solid Electric Cyan */
        color: #070B19 !important; /* Deep Navy Text */
        -webkit-text-fill-color: #070B19 !important;
        font-family: 'Fira Code', monospace !important;
        font-weight: 800 !important;
        font-size: 1rem !important;
        border: none !important;
        border-radius: 2px !important;
        height: 3.2rem; 
        width: 100%;
        transition: all 0.3s ease !important;
    }
    .stButton button:hover {
        background-color: #00FF66 !important; /* Shifts to Neon Green */
        box-shadow: 0 0 15px rgba(0, 255, 102, 0.4) !important;
        transform: translateY(-2px);
    }

    /* Secondary Download / Outline Buttons */
    div[data-testid="stDownloadButton"] button {
        background-color: transparent !important;
        border: 1px solid #00FF66 !important;
        color: #00FF66 !important;
        -webkit-text-fill-color: #00FF66 !important;
    }
    div[data-testid="stDownloadButton"] button:hover {
        background-color: #00FF66 !important;
        color: #070B19 !important;
        -webkit-text-fill-color: #070B19 !important;
    }

    /* Metric Visuals */
    [data-testid="stMetricValue"] {
        font-family: 'Fira Code', monospace !important;
        color: #00FF66 !important; /* Neon Green Metrics */
        -webkit-text-fill-color: #00FF66 !important;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        text-shadow: 0 0 15px rgba(0, 255, 102, 0.3) !important;
    }
    [data-testid="stMetricLabel"] { 
        color: #FFFFFF !important; 
        font-family: 'Inter', sans-serif !important;
    }

    /* Threat Alert Containers */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid #FF3366 !important; /* Alert Red */
        background-color: rgba(255, 51, 102, 0.05) !important;
        border-left: 4px solid #FF3366 !important;
    }

    /* Dataframes and Tables */
    [data-testid="stDataFrame"] { background-color: #0F1423 !important; }
    .stDataFrame th { 
        color: #00E5FF !important; 
        -webkit-text-fill-color: #00E5FF !important;
        font-family: 'Fira Code', monospace !important; 
        font-weight: 700 !important;
    }
    .stDataFrame td { 
        color: #FFFFFF !important; 
        -webkit-text-fill-color: #FFFFFF !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Hide Native UI Mechanics */
    #MainMenu, footer, header {visibility: hidden;}
    [data-testid="stSidebarCollapsedControl"], button[aria-label="Close sidebar"], button[aria-label="Open sidebar"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. STATE MANAGEMENT ---
if "logs" not in st.session_state: st.session_state.logs = []
if "payload" not in st.session_state: st.session_state.payload = ""
if "findings" not in st.session_state: st.session_state.findings = []
if "fixed" not in st.session_state: st.session_state.fixed = False
if "scan_name" not in st.session_state: st.session_state.scan_name = ""

# --- 4. ENGINE (REGEX LOCKED) ---
def run_audit(code):
    detected = []
    score = 100
    lines = code.splitlines()
    
    for idx, line in enumerate(lines, 1):
        if "os.getenv" in line or "os.environ" in line:
            continue
            
        aws_match = re.search(r'AKIA[0-9A-Z]{16}', line)
        if aws_match:
            detected.append({"type": "AWS_ACCESS_KEY", "line": idx, "token": aws_match.group(0)})
            score -= 40
            continue
            
        gcp_match = re.search(r'AIza[0-9A-Za-z-_]{35}', line)
        if gcp_match:
            detected.append({"type": "GCP_API_KEY", "line": idx, "token": gcp_match.group(0)})
            score -= 40
            continue
            
        secret_match = re.search(r'(?i)(api_key|apikey|password|passwd|pwd|secret|token|auth)\s*[:=]\s*([\'"][^\'"]+[\'"])', line)
        if secret_match:
            var_type = secret_match.group(1).upper()
            token = secret_match.group(2)
            detected.append({"type": f"HARDCODED_SECRET_{var_type}", "line": idx, "token": token})
            score -= 30

    return detected, max(score, 0)

# --- 5. FLAWLESS PATCH INTEGRATION ---
def apply_remediation(code, findings):
    lines = code.splitlines()
    
    for f in findings:
        idx = f['line'] - 1
        line = lines[idx]
        
        if f['type'] == "AWS_ACCESS_KEY":
            lines[idx] = line.replace(f['token'], 'os.getenv("AWS_ACCESS_KEY_ID")')
        elif f['type'] == "GCP_API_KEY":
            lines[idx] = line.replace(f['token'], 'os.getenv("GCP_API_KEY")')
        elif "HARDCODED_SECRET_" in f['type']:
            var_name = f['type'].replace("HARDCODED_SECRET_", "")
            lines[idx] = line.replace(f['token'], f'os.getenv("{var_name}")')
            
    output_code = "\n".join(lines)
    if "import os" not in output_code:
        output_code = "import os\n" + output_code
    return output_code

# --- 6. TERMINAL SIDEBAR ---
with st.sidebar:
    st.markdown("<div class='brand-sidebar'>SENTINEL</div>", unsafe_allow_html=True)
    st.markdown("<span style='color:#00E5FF; font-family:Fira Code; font-size: 0.9rem;'>SYS_STATUS: [SECURE_LINK]</span>", unsafe_allow_html=True)
    st.divider()
    
    st.markdown("### AUDIT LEDGER")
    if not st.session_state.logs:
        st.caption("No historical telemetry found.")
    else:
        for i, log in enumerate(st.session_state.logs):
            with st.expander(f"{log['name']} [{log['score']}%]"):
                st.caption(f"Status: {log['status']}")
                if st.button("LOAD TARGET", key=f"res_{i}"):
                    st.session_state.payload = log['content']
                    st.session_state.findings = []
                    st.session_state.fixed = False
                    st.rerun()
                    
    st.divider()
    st.markdown("### COMMIT PROFILE")
    st.session_state.scan_name = st.text_input("ASSIGN ALIAS:", value=f"BUILD_SCAN_v{len(st.session_state.logs) + 1}")
    
    if st.button("SAVE TELEMETRY"):
        if st.session_state.payload:
            current_status = "CRITICAL" if st.session_state.findings else "SECURE"
            current_score = 100 - (len(st.session_state.findings) * 30)
            st.session_state.logs.append({
                "name": st.session_state.scan_name,
                "content": st.session_state.payload,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": current_status,
                "score": max(current_score, 0)
            })
            st.rerun()

# --- 7. MAIN INTERFACE ---
tabs = st.tabs(["[ NEURAL DIAGNOSTIC ]", "[ COMPLIANCE MATRIX ]", "[ RISK TELEMETRY ]"])

# TAB 1: CORE AUDIT
with tabs[0]:
    col_left, col_right = st.columns([2.5, 1.5], gap="large")
    
    with col_left:
        st.markdown("### INGEST STREAM")
        input_type = st.radio("VECTOR:", ["RAW SOURCE", "FILE UPLOAD"], horizontal=True, label_visibility="collapsed")
        
        if input_type == "RAW SOURCE":
            st.session_state.payload = st.text_area("INJECT PAYLOAD:", value=st.session_state.payload, height=450)
        else:
            uploaded_file = st.file_uploader("UPLOAD TARGET FILE", type=["py", "js", "txt", "env"])
            if uploaded_file:
                st.session_state.payload = uploaded_file.getvalue().decode()
                
    with col_right:
        st.markdown("### EXECUTION PROTOCOL")
        if st.button("INITIATE SCAN"):
            if st.session_state.payload:
                st.session_state.findings, health_score = run_audit(st.session_state.payload)
                st.session_state.fixed = False
                st.metric("INTEGRITY INDEX", f"{health_score}%")
            else:
                st.error("ERR: NULL PAYLOAD.")
                
        if st.session_state.findings:
            st.markdown("### DETECTED ANOMALIES")
            for item in st.session_state.findings:
                with st.container(border=True):
                    st.markdown(f"<span style='color:#FF3366; font-family:Fira Code; font-weight:700;'>{item['type']}</span>", unsafe_allow_html=True)
                    st.markdown(f"**LINE:** `{item['line']}`")
                    
            st.divider()
            if st.button("DEPLOY HOTFIX"):
                st.session_state.payload = apply_remediation(st.session_state.payload, st.session_state.findings)
                st.session_state.findings = []
                st.session_state.fixed = True
                st.success("SYS: VULNERABILITIES NEUTRALIZED.")
                st.rerun()
                
        if st.session_state.fixed:
            st.download_button("DOWNLOAD SECURE BUILD", st.session_state.payload, "sentinel_secure.py")
        elif st.session_state.payload and not st.session_state.findings:
            st.info("SYS: SYSTEM OPTIMAL. ZERO ANOMALIES DETECTED.")

# TAB 2: COMPLIANCE MATRIX
with tabs[1]:
    st.markdown("### ISO/SOC2 LEDGER")
    if st.session_state.logs:
        log_records = pd.DataFrame(st.session_state.logs)
        m1, m2, m3 = st.columns(3)
        m1.metric("TOTAL SCANS", len(log_records))
        m2.metric("SECURE BUILDS", len(log_records[log_records['status'] == 'SECURE']))
        m3.metric("AVG INTEGRITY", f"{log_records['score'].mean():.1f}%")
        
        st.divider()
        st.markdown("#### RAW DATA STREAM")
        table_presentation = log_records[['date', 'name', 'status', 'score']].copy()
        table_presentation.columns = ["TIMESTAMP", "DUMP ALIAS", "SECURITY STATUS", "SCORE"]
        st.dataframe(table_presentation, use_container_width=True, hide_index=True)
    else:
        st.caption("SYS: NO DATA FOUND. INITIATE SCAN TO GENERATE MATRIX.")

# TAB 3: TELEMETRY
with tabs[2]:
    st.markdown("### RISK TELEMETRY")
    if st.session_state.logs:
        log_records = pd.DataFrame(st.session_state.logs)
        chart_data = log_records[['name', 'score']].copy()
        chart_data.columns = ["DUMP ALIAS", "INTEGRITY SCORE"]
        st.area_chart(chart_data, x="DUMP ALIAS", y="INTEGRITY SCORE", height=400)
    else:
        st.caption("SYS: INSUFFICIENT DATA FOR VISUALIZATION.")
