import streamlit as st
import re
import pandas as pd
from datetime import datetime

# --- 1. CORE SYSTEM CONFIG ---
st.set_page_config(
    page_title="Sentinel AI | Celeris Labs", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. THE IRONCLAD LAYOUT LOCK CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; }
    
    /* ANCHOR SIDEBAR OPEN COCKPIT */
    [data-testid="stSidebar"] { 
        background-color: #F8FAFC !important; 
        border-right: 2px solid #E2E8F0; 
        min-width: 320px !important;
        max-width: 320px !important;
        transform: none !important;
        left: 0 !important;
    }
    
    /* ENFORCE MAIN CONTENT COMPLIANCE SECTION */
    [data-testid="stMainView"] {
        margin-left: 0px !important; 
    }
    
    /* DISABLE SIDEBAR CLOSING TRIGGERS COMPLETELY */
    [data-testid="stSidebarCollapsedControl"], 
    button[data-testid="stBaseButton-headerNoContext"],
    button[aria-label="Close sidebar"],
    button[aria-label="Open sidebar"] { 
        display: none !important; 
    }
    
    /* Text Visibility (Solid Dark Slate) */
    * { color: #0F172A !important; opacity: 1 !important; -webkit-text-fill-color: #0F172A !important; }
    
    .brand-sidebar { color: #0284C7 !important; font-weight: 900; font-size: 1.8rem; margin-bottom: 20px; }

    /* UI Layout Mechanics */
    .stTabs [data-baseweb="tab-list"] { background-color: #F1F5F9; border-radius: 10px; padding: 5px; }
    .stTabs [aria-selected="true"] { color: #FFFFFF !important; background-color: #0284C7 !important; border-radius: 8px; }
    textarea, input { background-color: #FFFFFF !important; border: 2px solid #CBD5E1 !important; border-radius: 8px !important; }
    
    .stButton button { background-color: #0284C7 !important; color: #FFFFFF !important; border-radius: 8px !important; font-weight: 700; border: none !important; height: 3.2rem; width: 100%; }
    div[data-testid="stDownloadButton"] button { background-color: #10B981 !important; color: white !important; }

    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. SESSION DATA STATE ---
if "logs" not in st.session_state: st.session_state.logs = []
if "payload" not in st.session_state: st.session_state.payload = ""
if "findings" not in st.session_state: st.session_state.findings = []
if "fixed" not in st.session_state: st.session_state.fixed = False

# --- 4. ENGINE LOGIC ---
def run_audit(code):
    detected = []
    score = 100
    patterns = {
        "AWS_KEY": r'AKIA[0-9A-Z]{16}',
        "GCP_KEY": r'AIza[0-9A-Za-z-_]{35}',
        "HARDCODED_SECRET": r'(?i)(api_key|password|secret|token|passwd|auth|key)\s*[:= ]\s*[\'"]([^\'"]+)[\'"]'
    }
    for key, pattern in patterns.items():
        matches = re.findall(pattern, code)
        if matches:
            detected.append({"type": key, "matches": matches})
            score -= 30
    return detected, max(score, 0)

def apply_remediation(code, findings):
    new_code = code
    for f in findings:
        if f['type'] == "AWS_KEY":
            new_code = re.sub(r'AKIA[0-9A-Z]{16}', 'os.getenv("AWS_KEY")', new_code)
        elif f['type'] == "GCP_KEY":
            new_code = re.sub(r'AIza[0-9A-Za-z-_]{35}', 'os.getenv("GCP_KEY")', new_code)
        elif f['type'] == "HARDCODED_SECRET":
            new_code = re.sub(r'(?i)(api_key|password|secret|token|passwd|auth|key)\s*[:= ]\s*[\'"]([^\'"]+)[\'"]', 
                               r'\1 = os.getenv("\1".upper())', new_code)
    if "import os" not in new_code: new_code = "import os\n" + new_code
    return new_code

def get_threat_intel(t_type):
    intel = {
        "AWS_KEY": {"sev": "CRITICAL", "impact": "Account Takeover", "fix": "Use Environment Variables."},
        "GCP_KEY": {"sev": "CRITICAL", "impact": "Data Exposure", "fix": "Restrict Key in GCP Console."},
        "HARDCODED_SECRET": {"sev": "HIGH", "impact": "Auth Bypass", "fix": "Move to Secret Manager."}
    }
    return intel.get(t_type, {"sev": "MEDIUM", "impact": "Information Leak", "fix": "Encrypt secret."})

# --- 5. PERMANENT CONTROL SIDEBAR ---
with st.sidebar:
    st.markdown("<div class='brand-sidebar'>SENTINEL AI</div>", unsafe_allow_html=True)
    st.markdown("#### AUDIT HISTORY")
    
    if not st.session_state.logs:
        st.info("No saved sessions.")
    else:
        for i, log in enumerate(st.session_state.logs):
            with st.expander(f"📁 {log['name']}"):
                if st.button("LOAD", key=f"ld_{i}"):
                    st.session_state.payload = log['content']
                    st.session_state.fixed = False
                    st.rerun()

    st.divider()
    if st.button("💾 SAVE CURRENT SESSION"):
        if st.session_state.payload:
            status = "Vulnerable" if st.session_state.findings else "Clean"
            st.session_state.logs.append({
                "name": f"Scan_{len(st.session_state.logs)+1}", 
                "content": st.session_state.payload, 
                "date": datetime.now().strftime("%H:%M"),
                "status": status
            })
            st.rerun()

# --- 6. CORE APP WORKSPACE ---
tabs = st.tabs(["🚀 NEURAL AUDIT", "🛡️ EXPLOITS", "📊 RISK", "📜 COMPLIANCE", "🌐 THREAT INTEL"])

with tabs[0]:
    c1, c2 = st.columns([2.5, 1.5], gap="large")
    with c1:
        mode = st.radio("Input Method:", ["Paste Code", "Upload File"], horizontal=True, label_visibility="collapsed")
        if mode == "Paste Code":
            st.session_state.payload = st.text_area("Source Code Canvas:", value=st.session_state.payload, height=450)
        else:
            up = st.file_uploader("Drop Code File (Up to 200 MB)", type=["py", "js", "txt", "env"])
            if up: st.session_state.payload = up.getvalue().decode()
            
    with c2:
        st.markdown("#### COMMAND CENTER")
        if st.button("START DIAGNOSTIC"):
            if st.session_state.payload:
                st.session_state.findings, score = run_audit(st.session_state.payload)
                st.session_state.fixed = False
                st.metric("HEALTH SCORE", f"{score}%")
            else: st.warning("Input required.")
        
        if st.session_state.findings:
            st.markdown("### 🚨 Threat Analysis")
            for f in st.session_state.findings:
                dtl = get_threat_intel(f['type'])
                with st.container(border=True):
                    st.error(f"**{f['type']}**")
                    st.markdown(f"**Severity:** {dtl['sev']} | **Impact:** {dtl['impact']}")
                    st.caption(f"Action: {dtl['fix']}")
            
            st.divider()
            if st.button("GENERATE SECURE PATCH"):
                st.session_state.payload = apply_remediation(st.session_state.payload, st.session_state.findings)
                st.session_state.fixed = True
                st.success("Remediation Complete!")
                st.rerun()
            
            if st.session_state.fixed:
                st.download_button("📥 DOWNLOAD FIXED CODE", st.session_state.payload, "remediated.py")
        else:
            if st.session_state.payload and not st.session_state.findings:
                st.info("Clean Audit. No vulnerabilities detected.")

with tabs[2]:
    st.markdown("### Risk Metrics Dashboard")
    if st.session_state.logs:
        df_risk = pd.DataFrame([{"Risk": 10 if l['status']=="Clean" else 40, "Scan": l['name']} for l in st.session_state.logs])
        st.bar_chart(df_risk, x="Scan", y="Risk")
    else: st.info("No data tracking profile built yet.")

with tabs[3]:
    st.markdown("### 📜 Compliance Reporting")
    if st.session_state.logs:
        names = [l['name'] for l in st.session_state.logs]
        selection = st.multiselect("Select Logs:", ["Select All"] + names)
        report = st.session_state.logs if "Select All" in selection else [l for l in st.session_state.logs if l['name'] in selection]
        if report: st.table(pd.DataFrame(report)[['name', 'date', 'status']])
    else: st.info("No logs available.")

with tabs[4]:
    st.markdown("### 🌐 Global Threat Intelligence")
    c_m1, c_m2 = st.columns(2)
    c_m1.metric("Recent CVEs", "142", "+12%")
    c_m2.metric("Active Botnets", "1.2k", "-4%")
    st.divider()
    st.table(pd.DataFrame({"Severity": ["High", "Critical"], "Threat": ["SQL Injection", "AWS Key Leak"], "Origin": ["RU", "CN"]}))
