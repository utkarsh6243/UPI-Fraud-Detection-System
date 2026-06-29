import streamlit as st
st.markdown("""
<style>

.stApp{

    background:#050816;

    overflow:hidden;

}

.stApp::before{

    content:"";

    position:fixed;

    width:700px;

    height:700px;

    background:#2563EB;

    filter:blur(180px);

    opacity:.18;

    top:-200px;

    left:-150px;

    animation:move1 18s infinite alternate;

}

.stApp::after{

    content:"";

    position:fixed;

    width:650px;

    height:650px;

    background:#06B6D4;

    filter:blur(180px);

    opacity:.15;

    bottom:-250px;

    right:-150px;

    animation:move2 20s infinite alternate;

}

@keyframes move1{

    from{

        transform:translate(0,0);

    }

    to{

        transform:translate(250px,180px);

    }

}

@keyframes move2{

    from{

        transform:translate(0,0);

    }

    to{

        transform:translate(-250px,-180px);

    }

}

</style>
""", unsafe_allow_html=True)
from streamlit_option_menu import option_menu
from components.dashboard import show_dashboard
from components.detect_fraud import show_detect_fraud
from components.analytics import show_analytics
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sqlite3
import joblib
import os
import time
from auth import login, logout

# ----------------------------
# PAGE CONFIGURATION
# ----------------------------

st.set_page_config(
    page_title="UPI AI Shield Pro",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# DATABASE CONNECTION
# ----------------------------

conn = sqlite3.connect(
    "transactions.db",
    check_same_thread=False
)

cursor = conn.cursor()

# ----------------------------
# LOGIN
# ----------------------------

if not login():
    st.stop()

# ----------------------------
# LOAD MODEL
# ----------------------------

MODEL_PATH = "models/fraud_model.pkl"

if os.path.exists(MODEL_PATH):

    model = joblib.load(MODEL_PATH)

else:

    st.error(
        "Model not found. Please run train_model.py"
    )

    st.stop()

# ----------------------------
# SIDEBAR SETTINGS
# ----------------------------

with st.sidebar:

    st.markdown("""
    <style>

    .sidebar-box{

        background:linear-gradient(180deg,#0F172A,#020617);

        padding:20px;

        border-radius:18px;

        text-align:center;

        margin-bottom:20px;

        border:1px solid rgba(255,255,255,.08);

    }

    .logo{

        font-size:60px;

    }

    .brand{

        font-size:28px;

        color:white;

        font-weight:bold;

    }

    .edition{

        color:#38BDF8;

        font-size:14px;

    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-box">

    <div class="logo">🛡️</div>

    <div class="brand">

    UPI AI Shield

    </div>

    <div class="edition">

    Enterprise Edition v2.0

    </div>

    </div>
    """, unsafe_allow_html=True)

    st.success("🟢 AI Engine Online")

    st.info(f"Logged in as **{st.session_state.name}**")

    dark_mode = st.toggle(
        "Dark Theme",
        value=True
    )

    logout()

    st.markdown("---")

    selected = option_menu(

        menu_title=None,

        options=[

            "Dashboard",

            "Detect Fraud",

            "Analytics",

            "Transaction History",

            "AI Monitoring"

        ],

        icons=[

            "house-fill",

            "shield-fill-check",

            "graph-up-arrow",

            "clock-history",

            "cpu"

        ],

        default_index=0,

        styles={

            "container":{

                "padding":"10px",

                "background-color":"#111827",

                "border-radius":"15px"

            },

            "icon":{

                "color":"#38BDF8",

                "font-size":"20px"

            },

            "nav-link":{

                "font-size":"18px",

                "padding":"14px",

                "margin":"4px",

                "border-radius":"12px",

                "--hover-color":"#1E293B"

            },

            "nav-link-selected":{

                "background":"linear-gradient(90deg,#2563EB,#06B6D4)",

                "color":"white"

            }

        }

    )

    st.markdown("---")

    st.markdown("### ⚡ System Status")

    st.metric("AI Accuracy", "99.43%")

    st.metric("Latency", "0.18 sec")

    st.metric("Model", "Healthy")

    st.progress(99)

    st.caption("Enterprise Security Platform")

    

# ----------------------------
# THEME
# ----------------------------

if dark_mode:

    BG = "#020617"
    CARD = "#0F172A"
    TEXT = "white"
    SUBTEXT = "#CBD5E1"

else:

    BG = "#F4F7FB"
    CARD = "white"
    TEXT = "#111827"
    SUBTEXT = "#475569"

# ----------------------------
# GLOBAL CSS
# ----------------------------

st.markdown(f"""
<style>

.stApp{{
background:{BG};
color:{TEXT};
}}

section[data-testid="stSidebar"]{{
background:#0F172A;
}}

.block-container{{
padding-top:2rem;
padding-bottom:2rem;
}}

.title{{
font-size:48px;
font-weight:bold;
color:#38BDF8;
}}

.subtitle{{
font-size:18px;
color:{SUBTEXT};
margin-bottom:20px;
}}

.metric-card{{
background:{CARD};
padding:25px;
border-radius:18px;
box-shadow:0px 8px 25px rgba(0,0,0,.18);
transition:.3s;
text-align:center;
}}

.metric-card:hover{{
transform:translateY(-4px);
box-shadow:0px 10px 30px rgba(56,189,248,.25);
}}

.card-title{{
font-size:18px;
color:{SUBTEXT};
}}

.card-value{{
font-size:38px;
font-weight:bold;
}}

</style>
""", unsafe_allow_html=True)

# ============================================================
# DASHBOARD
# ============================================================

# ============================================================
# DASHBOARD
# ============================================================

if selected == "Dashboard":

    show_dashboard(conn)

# ============================================================
# DETECT FRAUD
# ============================================================

elif selected == "Detect Fraud":

    show_detect_fraud(conn, model)
 # ============================================================
# ANALYTICS
# ============================================================

# ============================================================
# ANALYTICS
# ============================================================

elif selected == "Analytics":

    show_analytics(conn)

# ==========================
# TRANSACTION HISTORY
# ==========================

elif selected == "Transaction History":

    st.markdown("""
    <style>

    .title{
        font-size:34px;
        font-weight:700;
        color:#38BDF8;
    }

    .subtitle{
        color:#94A3B8;
        font-size:15px;
        margin-bottom:20px;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="title">Transaction History</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Search, Filter & Export Transactions</div>',
        unsafe_allow_html=True
    )

    st.divider()

    history = pd.read_sql_query(

        "SELECT * FROM transactions ORDER BY id DESC",

        conn

    )

    c1, c2, c3 = st.columns(3)

    with c1:

        status_filter = st.selectbox(

            "Status",

            ["All", "Fraud", "Safe"]

        )

    with c2:

        location_filter = st.selectbox(

            "Location",

            ["All"] + sorted(history["location"].unique().tolist())

        )

    with c3:

        search = st.text_input(

            "Search UPI ID"

        )

    filtered = history.copy()

    if status_filter != "All":

        filtered = filtered[
            filtered["status"] == status_filter
        ]

    if location_filter != "All":

        filtered = filtered[
            filtered["location"] == location_filter
        ]

    if search:

        filtered = filtered[
            filtered["upi_id"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

    st.markdown("### Summary")

    m1, m2, m3, m4 = st.columns(4)

    with m1:

        st.metric(
            "Transactions",
            len(filtered)
        )

    with m2:

        st.metric(
            "Fraud",
            len(
                filtered[
                    filtered["status"] == "Fraud"
                ]
            )
        )

    with m3:

        st.metric(
            "Safe",
            len(
                filtered[
                    filtered["status"] == "Safe"
                ]
            )
        )

    with m4:

        if len(filtered) > 0:

            st.metric(
                "Average Amount",
                f"₹{filtered['amount'].mean():,.0f}"
            )

        else:

            st.metric(
                "Average Amount",
                "₹0"
            )

    st.divider()

    st.dataframe(

        filtered,

        use_container_width=True,

        hide_index=True,

        height=500

    )

    csv = filtered.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(

        "Download CSV",

        csv,

        "transactioncsv.csv",

        "text/csv",

        use_container_width=True

    )