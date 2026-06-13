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

# --- 2. DEEP NAVY CSS ENGINE (CONTRAST & LAYOUT FIXED) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600;700&family=Inter:wght@400;600;800&display=swap');

    /* Global Base */
    .stApp {
        background-color: #070B19 !important; 
        color: #FFFFFF !important; 
        font-family: 'Inter', sans-serif !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0F1423 !important; 
        border-right: 1px solid #00E5FF !important; 
        min-width: 320px !important;
        max-width: 320px !important;
        transform: none !important;
        left: 0 !important;
    }
    
    [data-testid="stMainView"] { margin-left: 0px !important; }

    /* Headers & Typography */
    h1, h2, h3, h4, h5 {
        font-family: 'Fira Code', monospace !important;
        color: #00E5FF !important; 
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 700 !important;
    }
    
    /* FIX: Force all standard labels, captions, and radio text to be pure white and bold */
    label, p, span, .stMarkdown, .stCaption {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        opacity: 1 !important;
        font-weight: 600 !important;
    }
    
    .brand-sidebar { 
        color: #00FF66 !important; 
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
        color: #8892B0 !important;
        font-family: 'Fira Code', monospace !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        color: #FFFFFF !important; 
        -webkit-text-fill-color: #FFFFFF !important;
        border-bottom: 3px solid #00E5FF !important; 
        background-color: #0F1423 !important;
    }

    /* Input Fields */
    .stTextInput input, 
    .stTextArea textarea, 
    [data-baseweb="base-input"] input, 
    [data-baseweb="textarea"] textarea,
    textarea, input {
        background-color: #151A2C !important; 
        border: 1px solid #00E5FF !important; 
        color: #FFFFFF !important; 
        -webkit-text-fill-color: #FFFFFF !important; 
        font-family: 'Fira Code', monospace !important;
        font-size: 15px !important;
        font-weight: 600 !important; 
        border-radius: 2px !important;
    }
    
    .stTextInput input:focus, 
    .stTextArea textarea:focus {
        border-color: #00FF66 !important; 
        box-shadow: 0 0 12px rgba(0, 255, 102, 0.2) !important;
    }

    /* Core Action Buttons */
    .stButton button {
        background-color: #00E5FF !important; 
        color: #070B19 !important; 
        -webkit-text-fill-color: #070B19 !important;
        font-family: 'Fira Code', monospace !important;
        font-weight: 800 !important;
        font-size: 1rem !important;
        border: none !important;
        border-radius: 2px !important;
        height: 3.5rem; /* Slightly taller for impact */
        width: 100%;
        transition: all 0.3s ease !important;
        margin-top: 10px;
    }
    .stButton button:hover {
        background-color: #00FF66 !important; 
        box-shadow: 0 0 15px rgba(0, 255, 102, 0.4) !important;
        transform: translateY(-2px);
    }

    /* Secondary Buttons */
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

    /* Metrics */
    [data-testid="stMetricValue"] {
        font-family: 'Fira Code', monospace !important;
        color: #00FF66 !important; 
        -webkit-text-fill-color: #00FF66 !important;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        text-shadow: 0 0 15px rgba(0, 255, 102, 0.3) !important;
    }
    [data-testid="stMetricLabel"] { 
        color: #FFFFFF !important; 
        font-family: 'Inter', sans-serif !important;
    }

    /* Threat Alerts */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid #FF3366 !important; 
        background-color: rgba(255, 51, 102, 0.05) !important;
        border-left: 4px solid #FF3366 !important;
        padding: 15px !important;
        margin-bottom: 10px !important;
    }

    /* Tables */
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

    /* Hide Native UI */
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
        st.markdown("<span style='color:#FFFFFF; font-weight:bold;'>No historical telemetry found.</span>", unsafe_allow_html=True)
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

# TAB 1: CORE AUDIT (LAYOUT FIXED: Stacked Vertically for tight UI)
with tabs[0]:
    st.markdown("### INGEST STREAM")
    
    # Mode selector directly above input
    input_type = st.radio("VECTOR:", ["RAW SOURCE", "FILE UPLOAD"], horizontal=True)
    
    # Input Area takes full width
    if input_type == "RAW SOURCE":
        st.session_state.payload = st.text_area("INJECT PAYLOAD:", value=st.session_state.payload, height=400, label_visibility="collapsed")
    else:
        uploaded_file = st.file_uploader("UPLOAD TARGET FILE", type=["py", "js", "txt", "env"], label_visibility="collapsed")
        if uploaded_file:
            st.session_state.payload = uploaded_file.getvalue().decode()
            
    st.divider()
    
    # Execution Protocol stacked directly below input
    st.markdown("### EXECUTION PROTOCOL")
    
    c1, c2 = st.columns([1, 2]) # 1/3 for button, 2/3 for metric/results
    
    with c1:
        if st.button("INITIATE SCAN"):
            if st.session_state.payload:
                st.session_state.findings, health_score = run_audit(st.session_state.payload)
                st.session_state.fixed = False
                st.session_state.last_score = health_score
            else:
                st.error("ERR: NULL PAYLOAD.")
                
    with c2:
        if hasattr(st.session_state, 'last_score'):
            st.metric("INTEGRITY INDEX", f"{st.session_state.last_score}%")
            
    # Threats display cleanly below
    if st.session_state.findings:
        st.markdown("### DETECTED ANOMALIES")
        for item in st.session_state.findings:
            with st.container(border=True):
                st.markdown(f"<span style='color:#FF3366; font-family:Fira Code; font-weight:700;'>{item['type']}</span>", unsafe_allow_html=True)
                st.markdown(f"**LINE:** `{item['line']}`")
                
        if st.button("DEPLOY HOTFIX"):
            st.session_state.payload = apply_remediation(st.session_state.payload, st.session_state.findings)
            st.session_state.findings = []
            st.session_state.fixed = True
            st.success("SYS: VULNERABILITIES NEUTRALIZED.")
            st.rerun()
            
    if st.session_state.fixed:
        st.download_button("DOWNLOAD SECURE BUILD", st.session_state.payload, "sentinel_secure.py")
    elif st.session_state.payload and not st.session_state.findings and hasattr(st.session_state, 'last_score'):
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
        st.markdown("<span style='color:#FFFFFF; font-weight:bold;'>SYS: NO DATA FOUND. INITIATE SCAN TO GENERATE MATRIX.</span>", unsafe_allow_html=True)

# TAB 3: TELEMETRY
with tabs[2]:
    st.markdown("### RISK TELEMETRY")
    if st.session_state.logs:
        log_records = pd.DataFrame(st.session_state.logs)
        chart_data = log_records[['name', 'score']].copy()
        chart_data.columns = ["DUMP ALIAS", "INTEGRITY SCORE"]
        st.area_chart(chart_data, x="DUMP ALIAS", y="INTEGRITY SCORE", height=400)
    else:
        st.markdown("<span style='color:#FFFFFF; font-weight:bold;'>SYS: INSUFFICIENT DATA FOR VISUALIZATION.</span>", unsafe_allow_html=True)
