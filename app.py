import streamlit as st
import re
import pandas as pd
from datetime import datetime

# --- CORE SYSTEM CONFIG ---
st.set_page_config(
    page_title="Sentinel AI", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- THE IRONCLAD LAYOUT LOCK CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; }
    
    /* SIDEBAR CONTAINER Mechanics */
    [data-testid="stSidebar"] { 
        background-color: #F8FAFC !important; 
        border-right: 2px solid #E2E8F0; 
        min-width: 320px !important;
        max-width: 320px !important;
        transform: none !important;
        left: 0 !important;
    }
    
    [data-testid="stMainView"] { margin-left: 0px !important; }
    
    /* DISABLE SIDEBAR CLOSING MECHANICS */
    [data-testid="stSidebarCollapsedControl"], 
    button[data-testid="stBaseButton-headerNoContext"],
    button[aria-label="Close sidebar"],
    button[aria-label="Open sidebar"] { 
        display: none !important; 
    }
    
    /* Text Visibility and Global Color Enforcement */
    * { color: #0F172A !important; opacity: 1 !important; -webkit-text-fill-color: #0F172A !important; }
    
    .brand-sidebar { color: #0284C7 !important; font-weight: 900; font-size: 1.8rem; margin-bottom: 20px; }

    /* UI Structural Styling */
    .stTabs [data-baseweb="tab-list"] { background-color: #F1F5F9; border-radius: 10px; padding: 5px; }
    .stTabs [aria-selected="true"] { color: #FFFFFF !important; background-color: #0284C7 !important; border-radius: 8px; }
    textarea, input { background-color: #FFFFFF !important; border: 2px solid #CBD5E1 !important; border-radius: 8px !important; }
    
    .stButton button { background-color: #0284C7 !important; color: #FFFFFF !important; border-radius: 8px !important; font-weight: 700; border: none !important; height: 3.2rem; width: 100%; }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- SESSION DATA STATE ---
if "logs" not in st.session_state: st.session_state.logs = []
if "payload" not in st.session_state: st.session_state.payload = ""
if "findings" not in st.session_state: st.session_state.findings = []
if "fixed" not in st.session_state: st.session_state.fixed = False
if "custom_scan_name" not in st.session_state: st.session_state.custom_scan_name = ""

# --- LINE-BY-LINE AUDIT ENGINE (FIXES RECURSIVE ERROR) ---
def run_audit(code):
    detected = []
    score = 100
    lines = code.splitlines()
    
    for idx, line in enumerate(lines, 1):
        # Rule 1: Completely skip evaluation if line contains environment mapping functions
        if "os.getenv" in line or "os.environ" in line or "getenv" in line:
            continue
            
        # Rule 2: Evaluate for explicit AWS Credentials
        aws_match = re.search(r'AKIA[0-9A-Z]{16}', line)
        if aws_match:
            detected.append({"type": "AWS_KEY", "line": idx, "token": aws_match.group(0)})
            score -= 30
            continue
            
        # Rule 3: Evaluate for explicit GCP Credentials
        gcp_match = re.search(r'AIza[0-9A-Za-z-_]{35}', line)
        if gcp_match:
            detected.append({"type": "GCP_KEY", "line": idx, "token": gcp_match.group(0)})
            score -= 30
            continue
            
        # Rule 4: General Secret Configuration Keys
        secret_match = re.search(r'(?i)\b(api_key|password|secret|token|passwd|auth|key)\b\s*[:= ]\s*[\'"]([^\'"]+)[\'"]', line)
        if secret_match:
            var_label = secret_match.group(1)
            secret_val = secret_match.group(2)
            
            # Skip if value assigned matches variable label configuration markers
            if secret_val.strip().upper() in [var_label.strip().upper(), "AWS_KEY", "GCP_KEY"]:
                continue
                
            detected.append({"type": "HARDCODED_SECRET", "line": idx, "token": secret_val})
            score -= 30

    return detected, max(score, 0)

def apply_remediation(code, findings):
    new_lines = code.splitlines()
    for f in findings:
        idx = f['line'] - 1
        line = new_lines[idx]
        
        if f['type'] == "AWS_KEY":
            new_lines[idx] = re.sub(r'AKIA[0-9A-Z]{16}', 'os.getenv("AWS_KEY")', line)
        elif f['type'] == "GCP_KEY":
            new_lines[idx] = re.sub(r'AIza[0-9A-Za-z-_]{35}', 'os.getenv("GCP_KEY")', line)
        elif f['type'] == "HARDCODED_SECRET":
            new_lines[idx] = re.sub(r'(?i)(api_key|password|secret|token|passwd|auth|key)\s*[:= ]\s*[\'"]([^\'"]+)[\'"]', 
                                   r'\1 = os.getenv("\1".upper())', line)
            
    output_code = "\n".join(new_lines)
    if "import os" not in output_code:
        output_code = "import os\n" + output_code
    return output_code

# --- AUDIT CONTROL SIDEBAR ---
with st.sidebar:
    st.markdown("<div class='brand-sidebar'>SENTINEL AI</div>", unsafe_allow_html=True)
    st.markdown("#### HISTORICAL AUDITS")
    
    if not st.session_state.logs:
        st.caption("No historical sessions compiled.")
    else:
        for i, log in enumerate(st.session_state.logs):
            with st.expander(f"Record: {log['name']}"):
                st.caption(f"Status: {log['status']}")
                st.caption(f"Score: {log['score']}%")
                if st.button("RESTORE DATA", key=f"restore_{i}"):
                    st.session_state.payload = log['content']
                    st.session_state.findings = []
                    st.session_state.fixed = False
                    st.rerun()
                    
    st.divider()
    st.markdown("#### LOG PRODUCTION")
    st.session_state.custom_scan_name = st.text_input("Assign Target Name:", value=f"Production_Scan_{len(st.session_state.logs) + 1}")
    
    if st.button("COMMIT SCAN TO PROFILE"):
        if st.session_state.payload:
            current_status = "Vulnerable" if st.session_state.findings else "Clean"
            current_score = 100 - (len(st.session_state.findings) * 30)
            st.session_state.logs.append({
                "name": st.session_state.custom_scan_name,
                "content": st.session_state.payload,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "status": current_status,
                "score": max(current_score, 0)
            })
            st.rerun()

# --- WORKSPACE AREA ---
tabs = st.tabs(["NEURAL AUDIT ENGINE", "ENTERPRISE COMPLIANCE MATRIX"])

# TAB 1: Core Scan Diagnostics and Area Trend Mapping
with tabs[0]:
    col_left, col_right = st.columns([2.6, 1.4], gap="large")
    
    with col_left:
        st.markdown("#### SCAN UTILITY")
        input_type = st.radio("Upload Mechanism:", ["Paste Text Source", "Upload Local File"], horizontal=True, label_visibility="collapsed")
        
        if input_type == "Paste Text Source":
            st.session_state.payload = st.text_area("Source Code Area:", value=st.session_state.payload, height=420)
        else:
            uploaded_file = st.file_uploader("Select Target Source File:", type=["py", "js", "txt", "env"])
            if uploaded_file:
                st.session_state.payload = uploaded_file.getvalue().decode()
                
    with col_right:
        st.markdown("#### CORE EXECUTION")
        if st.button("EXECUTE ANALYSIS"):
            if st.session_state.payload:
                st.session_state.findings, health_score = run_audit(st.session_state.payload)
                st.session_state.fixed = False
                st.metric("COMPLIANCE HEALTH SCORE", f"{health_score}%")
            else:
                st.error("No source code detected to process.")
                
        if st.session_state.findings:
            st.markdown("#### DETECTED EXPLOITS")
            for item in st.session_state.findings:
                with st.container(border=True):
                    st.markdown(f"**Vulnerability Class:** {item['type']}")
                    st.markdown(f"**Line Registration:** {item['line']}")
                    
            st.divider()
            if st.button("DEPLOY INTEGRAL REMEDIATION"):
                st.session_state.payload = apply_remediation(st.session_state.payload, st.session_state.findings)
                st.session_state.findings = []
                st.session_state.fixed = True
                st.success("Remediation execution complete. Threat registers clear.")
                st.rerun()
                
        if st.session_state.fixed:
            st.download_button("DOWNLOAD DISINFECTED FILE", st.session_state.payload, "remediated_source.py")

# TAB 2: Clean, Formatted Reporting Profile
with tabs[1]:
    st.markdown("### COMPLIANCE AUDIT AUDIT METRICS")
    
    if st.session_state.logs:
        log_records = pd.DataFrame(st.session_state.logs)
        
        # High Level Metric Summary Panels
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        metric_col1.metric("Evaluations Registered", len(log_records))
        metric_col2.metric("Uncompromised Builds", len(log_records[log_records['status'] == 'Clean']))
        metric_col3.metric("System Mean Health Metric", f"{log_records['score'].mean():.1f}%")
        
        st.divider()
        
        # Risk Distribution Curve (Area Trend Chart replacing basic bar charts)
        st.markdown("#### INTER-SESSION RISK PROFILE TREND")
        chart_data = log_records[['name', 'score']].copy()
        chart_data.columns = ["Session Identity", "Security Health Index"]
        st.area_chart(chart_data, x="Session Identity", y="Security Health Index")
        
        st.divider()
        
        # Formal Reporting Matrix Display Table
        st.markdown("#### HISTORICAL REPORT DATA TABLE")
        table_presentation = log_records[['name', 'date', 'status', 'score']].copy()
        table_presentation.columns = ["Session Identifier", "Timestamp Registered", "Operational Assessment", "Health Score Index"]
        st.dataframe(table_presentation, use_container_width=True, hide_index=True)
        
    else:
        st.info("No active log signatures stored inside session buffer memory. Execute and commit a scan to access metrics.")
