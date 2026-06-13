# --- 2. HIGH-VISIBILITY GALACTIC CSS ENGINE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Rajdhani:wght@500;600;700&display=swap');

    /* Global Cosmic Background */
    .stApp {
        background: #05010F !important; /* Darker, solid background for contrast */
        color: #FFFFFF !important; /* Pure white body text */
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 16px !important;
    }

    /* Frosted Glass Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(10, 5, 20, 0.85) !important; /* Less transparent for readability */
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
        color: #FFFFFF !important; /* Pure white active tab */
        border-bottom: 4px solid #00F0FF !important;
        background: rgba(0, 240, 255, 0.1) !important;
        text-shadow: 0 0 8px rgba(0, 240, 255, 0.6);
    }

    /* Terminal Text Areas & Inputs - MAXIMUM READABILITY */
    textarea, input {
        background: #080318 !important; /* Solid dark background */
        border: 2px solid rgba(0, 240, 255, 0.5) !important;
        color: #FFFFFF !important; /* Pure white code text */
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
