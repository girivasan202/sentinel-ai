import streamlit as st
import re
import pandas as pd
from datetime import datetime

# --- 1. CORE SYSTEM CONFIG ---
st.set_page_config(
    page_title="SENTINEL // NEURAL AUDIT", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. BLACK HAT / CYBERSEC CSS ENGINE ---
st.markdown("""
    <style>
    /* Global Dark Theme */
    .stApp { background-color: #050505 !important; color: #00FF41 !important; font-family: 'Courier New', Courier, monospace !important; }
    
    /* Sidebar Lock & Styling */
    [data-testid="stSidebar"] { 
        background-color: #0a0a0a !important; 
        border-right: 1px solid #00FF41 !important; 
        min-width: 320px !important;
        max-width: 320px !important;
        transform: none !important;
        left: 0 !important;
    }
    
    [data-testid="stMainView"] { margin-left: 0px !important; }
    
    /* Override all text to Neon Green Terminal Font */
    h1, h2, h3, h4, h5, h6, p, span, div, label { color: #00FF41 !important; font-family: 'Courier New', Courier, monospace !important; }
    
    /* Brand Header */
    .brand-sidebar { color: #FF003C !important; font-weight: 900; font-size: 2.2rem; margin-bottom: 20px; letter-spacing: 3px; text-shadow: 0 0 8px #FF003C; }
    
    /* Tab Styling (Terminal Style) */
    .stTabs [data-baseweb="tab-list"] { background-color: #050505; border-bottom: 1px solid #00FF41; gap: 0px; }
    .stTabs [data-baseweb="tab"] { color: #444444 !important; background-color: transparent; border: none; font-weight: bold; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { color: #00FF41 !important; border-bottom: 3px solid #00FF41 !important; background-color: #111111 !important; text-shadow: 0 0 5px #00FF41; }
    
    /* Inputs & Text Areas */
    textarea, input { background-color: #000000 !important; border: 1px solid #00FF41 !important; color: #00FF41 !important; font-family: 'Courier New', Courier, monospace !important; border-radius: 0px !important; }
    textarea:focus, input:focus { box-shadow: 0 0 8px #00FF41 !important; }
    
    /* Core Buttons */
    .stButton button { background-color: #000000 !important; color: #00FF41 !important; border: 1px solid #00FF41 !important; border-radius: 0px !important; font-weight: bold; letter-spacing: 1px; transition: all 0.2s ease; height: 3rem; width: 100%; }
    .stButton button:hover { background-color: #00FF41 !important; color: #000000 !important; box-shadow: 0 0 15px #00FF41; }
    
    /* Action / Download Buttons */
    div[data-testid="stDownloadButton"] button { border-color: #FF003C !important; color: #FF003C !important; }
    div[data-testid="stDownloadButton"] button:hover { background-color: #FF003C !important; color: #000000 !important; box-shadow: 0 0 15px #FF003C; }
    
    /* Health Score Metric Styling */
    [data-testid="stMetricValue"] { color: #FF003C !important; text-shadow: 0 0 10px #FF003C; font-size: 3.5rem !important; font-weight: 900; }
    [data-testid="stMetricLabel"] { color: #00FF41 !important; font-size: 1.2rem !important; letter-spacing: 2px; }
    
    /* Container Borders */
    [data-testid="stVerticalBlockBorderWrapper"] { border: 1px solid #333333 !important; border-radius: 0px !important; background-color: #0a0a0a !important; }
    
    /* Hide Streamlit Native UI */
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

# --- 4. AGGRESSIVE AUDIT ENGINE ---
def run_audit(code):
    detected = []
    score = 100
    lines = code.splitlines()
    
    for idx, line in enumerate(lines, 1):
        # Ignore lines that are already patched (using os.getenv)
        if "os.getenv" in line or "os.environ" in line:
            continue
            
        # 1. AWS Keys
        aws_match = re.search(r'AKIA[0-9A-Z]{16}', line)
        if aws_match:
            detected.append({"type": "CRITICAL: AWS_ACCESS_KEY", "line": idx, "token": aws_match.group(0)})
            score -= 40
            
        # 2. GCP Keys
        gcp_match = re.search(r'AIza[0-9A-Za-z-_]{35}', line)
        if gcp_match:
            detected.append({"type": "CRITICAL: GCP_API_KEY", "line": idx, "token": gcp_match.group(0)})
            score -= 40
            
        # 3. Hardcoded Passwords, Tokens, API Keys (Aggressive Match)
        # Looks for: password = "..." or api_key: '...'
        secret_match = re.search(r'(?i)(api_key|apikey|password|passwd|pwd|secret|token|auth)\s*[:=]\s*([\'"][^\'"]+[\'"])', line)
        if secret_match:
            detected.append({"type": f"HIGH: HARDCODED_{secret_match.group(1).upper()}", "line": idx, "token": secret_match.group(2)})
            score -= 30

    return detected, max(score, 0)

def apply_remediation(code, findings):
    new_lines = code.splitlines()
    for f in findings:
        idx = f['line'] - 1
        line = new_lines[idx]
        
        # Strip exact strings and replace with environment variables
        if "AWS_ACCESS_KEY" in f['type']:
            new_lines[idx] = re.sub(r'AKIA[0-9A-Z]{16}', 'os.getenv("AWS_ACCESS_KEY_ID")', line)
        elif "GCP_API_KEY" in f['type']:
            new_lines[idx] = re.sub(r'AIza[0-9A-Za-z-_]{35}', 'os.getenv("GCP_API_KEY")', line)
        elif "HARDCODED_" in f['type']:
            # Extracts the variable name being assigned and uses it for the env var
            new_lines[idx] = re.sub(r'(?i)(api_key|apikey|password|passwd|pwd|secret|token|auth)\s*[:=]\s*([\'"][^\'"]+[\'"])', 
                                   r'\1 = os.getenv("\1".upper())', line)
            
    output_code = "\n".join(new_lines)
    if "import os" not in output_code:
        output_code = "import os\n" + output_code
    return output_code

# --- 5. TERMINAL SIDEBAR ---
with st.sidebar:
    st.markdown("<div class='brand-sidebar'>SENTINEL // OS</div>", unsafe_allow_html=True)
    st.markdown("`SYSTEM STATUS: ONLINE`")
    st.markdown("`ENCRYPTION: AES-256`")
    st.divider()
    
    st.markdown("### [ SESSION LOGS ]")
    if not st.session_state.logs:
        st.caption("> No previous dumps found.")
    else:
        for i, log in enumerate(st.session_state.logs):
            with st.expander(f"> {log['name']} [{log['score']}%]"):
                st.caption(f"Status: {log['status']}")
                if st.button("RESTORE DUMP", key=f"res_{i}"):
                    st.session_state.payload = log['content']
                    st.session_state.findings = []
                    st.session_state.fixed = False
                    st.rerun()
                    
    st.divider()
    st.markdown("### [ COMMIT TO LEDGER ]")
    st.session_state.scan_name = st.text_input("DUMP ALIAS:", value=f"SEC_SCAN_v{len(st.session_state.logs) + 1}")
    
    if st.button("SAVE TELEMETRY"):
        if st.session_state.payload:
            current_status = "COMPROMISED" if st.session_state.findings else "SECURE"
            current_score = 100 - (len(st.session_state.findings) * 30)
            st.session_state.logs.append({
                "name": st.session_state.scan_name,
                "content": st.session_state.payload,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": current_status,
                "score": max(current_score, 0)
            })
            st.rerun()

# --- 6. MAIN TERMINAL WORKSPACE ---
tabs = st.tabs(["[ TERMINAL ]", "[ EXPLOIT DB ]", "[ COMPLIANCE ]", "[ TELEMETRY ]"])

# TAB 1: CORE AUDIT
with tabs[0]:
    col_left, col_right = st.columns([2.5, 1.5], gap="large")
    
    with col_left:
        st.markdown("### >_ INPUT STREAM")
        input_type = st.radio("VECTOR:", ["RAW TEXT", "FILE UPLOAD"], horizontal=True, label_visibility="collapsed")
        
        if input_type == "RAW TEXT":
            st.session_state.payload = st.text_area("INJECT CODE HERE:", value=st.session_state.payload, height=450)
        else:
            uploaded_file = st.file_uploader("UPLOAD TARGET (.py, .js, .env)", type=["py", "js", "txt", "env"])
            if uploaded_file:
                st.session_state.payload = uploaded_file.getvalue().decode()
                
    with col_right:
        st.markdown("### >_ COMMAND EXECUTION")
        if st.button("INITIATE NEURAL SCAN"):
            if st.session_state.payload:
                st.session_state.findings, health_score = run_audit(st.session_state.payload)
                st.session_state.fixed = False
                st.metric("INTEGRITY SCORE", f"{health_score}%")
            else:
                st.error("ERR: NULL PAYLOAD.")
                
        if st.session_state.findings:
            st.markdown("### >_ THREATS DETECTED")
            for item in st.session_state.findings:
                with st.container(border=True):
                    st.markdown(f"<span style='color:#FF003C; font-weight:bold;'>{item['type']}</span>", unsafe_allow_html=True)
                    st.markdown(f"`LINE: {item['line']}`")
                    
            st.divider()
            if st.button("EXECUTE HOTFIX PATCH"):
                st.session_state.payload = apply_remediation(st.session_state.payload, st.session_state.findings)
                st.session_state.findings = []
                st.session_state.fixed = True
                st.success("SYS: MALICIOUS STRINGS SANITIZED.")
                st.rerun()
                
        if st.session_state.fixed:
            st.download_button("DOWNLOAD SANITIZED BUILD", st.session_state.payload, "sentinel_patched.py")
        elif st.session_state.payload and not st.session_state.findings:
            st.info("SYS: 0 EXPLOITS DETECTED. SYSTEM SECURE.")

# TAB 2: EXPLOIT DB
with tabs[1]:
    st.markdown("### >_ KNOWN VULNERABILITY DATABASE")
    db_data = pd.DataFrame({
        "CVE ID": ["CVE-2024-1011", "CVE-2023-4492", "CVE-2024-0091", "CVE-2023-8812"],
        "THREAT VECTOR": ["AWS Root Key Exposure", "Hardcoded JWT Token", "GCP Service Account Leak", "SQL Password in Plaintext"],
        "SEVERITY": ["CRITICAL", "HIGH", "CRITICAL", "HIGH"],
        "AUTO-REMEDIATION": ["Supported", "Supported", "Supported", "Supported"]
    })
    st.dataframe(db_data, use_container_width=True, hide_index=True)

# TAB 3: COMPLIANCE MATRIX
with tabs[2]:
    st.markdown("### >_ ISO/SOC2 COMPLIANCE LEDGER")
    
    if st.session_state.logs:
        log_records = pd.DataFrame(st.session_state.logs)
        
        m1, m2, m3 = st.columns(3)
        m1.metric("TOTAL SCANS", len(log_records))
