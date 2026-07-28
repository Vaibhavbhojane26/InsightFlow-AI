import streamlit as st
import pandas as pd


from modules.dashboard import dashboard_page
from database.database import initialize_database
from modules.auth import initialize_auth
from modules.upload import upload_dataset
from modules.profiling import dataset_profile
from modules.cleaning import clean_dataset
from modules.analysis import analyze_dataset
from modules.visualization import visualize_dataset
from modules.insights import generate_insights
from modules.report import generate_pdf_report
from modules.export import (
    download_csv,
    download_excel
)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="InsightFlow AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# INITIALIZE SYSTEM
# ==========================================

initialize_database()


# ==========================================
# SESSION
# ==========================================

if "dataset" not in st.session_state:
    st.session_state.dataset = None

if "login" not in st.session_state:
    st.session_state.login = False

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

   

    st.title("📊 InsightFlow AI")

    st.caption(
        "Enterprise Data Intelligence Platform"
    )

    st.divider()

    menu = st.radio(

        "Navigation",

        [

            "🏠 Dashboard",

            "📂 Dataset",

            "🧹 Data Cleaning",

            "📈 Analysis",

            "📊 Visualization",

            "💡 AI Insights",

            "📄 Reports"

        ]

    )

    st.divider()

    st.success("Version 2.0")

    st.caption("Developed By")

    st.write("Vaibhav Bhojane")




# ==========================================
# DASHBOARD
# ==========================================

if not st.session_state.login:

    from modules.auth import login_required

    login_required()

if menu == "🏠 Dashboard":

    dashboard_page()



# ==========================================
# DATASET
# ==========================================

# ==========================================
# PROJECTS
# ==========================================




elif menu == "📂 Dataset":

    st.title("📂 Dataset Manager")

    df = upload_dataset()

    if df is not None:

        st.session_state.dataset = df

        st.success("Dataset Loaded Successfully")


# ==========================================
# DATA CLEANING
# ==========================================

elif menu == "🧹 Data Cleaning":

    st.title("🧹 Data Cleaning")

    if st.session_state.dataset is None:

        st.warning("Please upload a dataset first.")

    else:

        cleaned_df = clean_dataset(
            st.session_state.dataset
        )

        st.session_state.dataset = cleaned_df


# ==========================================
# ANALYSIS
# ==========================================

elif menu == "📈 Analysis":

    st.title("📈 Data Analysis")

    if st.session_state.dataset is None:

        st.warning("Please upload a dataset first.")

    else:

        dataset_profile(
            st.session_state.dataset
        )

        analyze_dataset(
            st.session_state.dataset
        )


# ==========================================
# VISUALIZATION
# ==========================================

elif menu == "📊 Visualization":

    st.title("📊 Data Visualization")

    if st.session_state.dataset is None:

        st.warning("Please upload a dataset first.")

    else:

        visualize_dataset(
            st.session_state.dataset
        )


# ==========================================
# AI INSIGHTS
# ==========================================

elif menu == "💡 AI Insights":

    st.title("💡 AI Insights")

    if st.session_state.dataset is None:

        st.warning("Please upload a dataset first.")

    else:

        generate_insights(
            st.session_state.dataset
        )


# ==========================================
# REPORTS
# ==========================================

elif menu == "📄 Reports":

    st.title("📄 Reports")

    if st.session_state.dataset is None:

        st.warning("Please upload a dataset first.")

    else:

        generate_pdf_report(
            st.session_state.dataset
        )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            download_csv(
                st.session_state.dataset
            )

        with col2:

            download_excel(
                st.session_state.dataset
            )

# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "InsightFlow AI v2.0 | Enterprise Data Intelligence Platform | Developed by Vaibhav Bhojane"
)

def load_css():
    with open("assets/styles.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()