import streamlit as st
import re
import pandas as pd
from datetime import datetime

# --- 1. CORE SYSTEM CONFIG ---
st.set_page_config(
    page_title="SENTINEL // GALACTIC", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. HIGH-VISIBILITY GALACTIC CSS ENGINE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Rajdhani:wght@500;600;700&display=swap');

    /* Global Cosmic Background */
    .stApp {
        background: #05010F !important; 
        color: #FFFFFF !important; 
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 16px !important;
    }

    /* Frosted Glass Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(10, 5, 20, 0.85) !important; 
        border-right: 2px solid rgba(0, 240, 255, 0.3) !important;
        min-width: 320px !important;
        max-width: 320px !important;
        transform: none !important;
        left: 0 !important;
    }
    
    [data-testid="stMainView"] { margin-left: 0px !important; }

    /* Sci-Fi Headings */
    h1, h2, h3, h4, h5 {
        font-family: 'Orbitron', sans-serif !important;
        color: #00F0FF !important;
        text-shadow: 0 0 8px rgba(0, 240, 255, 0.4);
        letter-spacing: 1px;
    }
    
    .brand-sidebar { 
        color: #B000FF !important; 
        font-family: 'Orbitron', sans-serif;
        font-weight: 900; 
        font-size: 2.2rem; 
        margin-bottom: 20px; 
        letter-spacing: 2px; 
        text-shadow: 0 0 10px #B000FF; 
    }

    /* Holographic Tabs - High Contrast */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent !important;
        border-bottom: 2px solid rgba(176, 0, 255, 0.4) !important;
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #A090B0 !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 1.1rem;
        font-weight: bold;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        color: #FFFFFF !important; 
        border-bottom: 4px solid #00F0FF !important;
        background: rgba(0, 240, 255, 0.1) !important;
        text-shadow: 0 0 8px rgba(0, 240, 255, 0.6);
    }

    /* Terminal Text Areas & Inputs - MAXIMUM READABILITY */
    textarea, input {
        background: #080318 !important; 
        border: 2px solid rgba(0, 240, 255, 0.5) !important;
        color: #FFFFFF !important; 
        font-family: 'Courier New', Courier, monospace !important;
        font-size: 15px !important;
        font-weight: bold !important;
        border-radius: 4px !important;
    }
    textarea:focus, input:focus {
        border-color: #B000FF !important;
        box-shadow: 0 0 10px rgba(176, 0, 255, 0.5) !important;
        background: #05010F !important;
    }

    /* Animated Gradient Buttons */
    .stButton button {
        background: linear-gradient(90deg, #4A00E0 0%, #8E2DE2 50%, #00F0FF 100%) !important;
        background-size: 200% auto !important;
        color: #FFFFFF !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 900 !important;
        font-size: 1.1rem !important;
        border: none !important;
        border-radius: 4px !important;
        height: 3.5rem; 
        width: 100%;
        transition: 0.4s !important;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .stButton button:hover {
        background-position: right center !important;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.6) !important;
        transform: scale(1.02);
    }

    /* Secondary Download Button */
    div[data-testid="stDownloadButton"] button {
        background: rgba(0, 240, 255, 0.1) !important;
        border: 2px solid #00F0FF !important;
        color: #FFFFFF !important;
    }
    div[data-testid="stDownloadButton"] button:hover {
        background: rgba(0, 240, 255, 0.3) !important;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.5) !important;
    }

    /* Glowing Health Metric */
    [data-testid="stMetricValue"] {
        font-family: 'Orbitron', sans-serif !important;
        color: #FFFFFF !important;
        text-shadow: 0 0 15px #B000FF !important;
        font-size: 3.5rem !important;
        font-weight: bold;
    }
    [data-testid="stMetricLabel"] { 
        color: #00F0FF !important; 
        font-size: 1.2rem !important; 
        font-family: 'Orbitron', sans-serif !important;
        font-weight: bold;
    }

    /* Threat Containers */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid rgba(255, 0, 60, 0.6) !important;
        background: rgba(255, 0, 60, 0.1) !important;
        border-radius: 4px !important;
    }

    /* Dataframe/Table Readability */
    [data-testid="stDataFrame"] {
        background-color: #080318 !important;
    }
    .stDataFrame th { color: #00F0FF !important; font-family: 'Orbitron', sans-serif !important; }
    .stDataFrame td { color: #FFFFFF !important; }

    /* Hide Native UI Mechanics */
    #MainMenu, footer, header {visibility: hidden;}
    [data-testid="stSidebarCollapsedControl"], button[aria-label="Close sidebar"], button[aria-label="Open sidebar"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if "logs" not in st.session_state: st.session_state.logs = []
if "payload" not in st.session_state: st.session_state.payload = ""
if "findings" not in st.session_state: st.session_state.findings = []
if "fixed" not in st.session_state: st.session_state.fixed = False
if "scan_name" not in st.session_state: st.session_state.scan_name = ""

# --- 4. BULLETPROOF AUDIT ENGINE ---
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

# --- 5. FLAWLESS REMEDIATION ENGINE ---
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

# --- 6. COMMAND SIDEBAR ---
with st.sidebar:
    st.markdown("<div class='brand-sidebar'>SENTINEL</div>", unsafe_allow_html=True)
    st.markdown("<span style='color:#00F0FF; font-family:Orbitron; font-weight:bold;'>SYS_STATUS: // ONLINE</span>", unsafe_allow_html=True)
    st.divider()
    
    st.markdown("### DATA LOGS")
    if not st.session_state.logs:
        st.caption("No historical telemetry found.")
    else:
        for i, log in enumerate(st.session_state.logs):
            with st.expander(f"{log['name']} [{log['score']}%]"):
                st.caption(f"Status: {log['status']}")
                if st.button("RESTORE", key=f"res_{i}"):
                    st.session_state.payload = log['content']
                    st.session_state.findings = []
                    st.session_state.fixed = False
                    st.rerun()
                    
    st.divider()
    st.markdown("### COMMIT PROFILE")
    st.session_state.scan_name = st.text_input("ASSIGN ALIAS:", value=f"STELLAR_SCAN_{len(st.session_state.logs) + 1}")
    
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
        st.markdown("### INPUT STREAM")
        input_type = st.radio("VECTOR:", ["RAW TEXT", "FILE UPLOAD"], horizontal=True, label_visibility="collapsed")
        
        if input_type == "RAW TEXT":
            st.session_state.payload = st.text_area("INJECT PAYLOAD:", value=st.session_state.payload, height=450)
        else:
            uploaded_file = st.file_uploader("UPLOAD TARGET FILE", type=["py", "js", "txt", "env"])
            if uploaded_file:
                st.session_state.payload = uploaded_file.getvalue().decode()
                
    with col_right:
        st.markdown("### COMMAND EXECUTION")
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
                    st.markdown(f"<span style='color:#FF003C; font-family:Orbitron; font-weight:bold;'>{item['type']}</span>", unsafe_allow_html=True)
                    st.markdown(f"**LINE REGISTRY:** `{item['line']}`")
                    
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
