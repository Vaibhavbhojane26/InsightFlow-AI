import streamlit as st
import pandas as pd


# ==========================================
# DASHBOARD PAGE
# ==========================================

def dashboard_page():

    st.title("🚀 InsightFlow AI")

    st.caption("Enterprise Data Intelligence Platform")

    st.divider()

    # ==========================================
    # DATASET CHECK
    # ==========================================

    if (
        "dataset" not in st.session_state
        or
        st.session_state.dataset is None
    ):

        st.info(
            "📂 Upload your first dataset from the Dataset menu to start analysis."
        )

        return

    # ==========================================
    # DATASET
    # ==========================================

    df = st.session_state.dataset

    rows = df.shape[0]

    cols = df.shape[1]

    missing = int(
        df.isnull().sum().sum()
    )

    duplicate = int(
        df.duplicated().sum()
    )

    quality = round(

        (
            (rows * cols - missing)
            /
            (rows * cols)
        ) * 100,

        2
    )

    # ==========================================
    # DATASET HEALTH
    # ==========================================

    if quality >= 90:
        health = "🟢 Excellent"

    elif quality >= 70:
        health = "🟡 Good"

    elif quality >= 50:
        health = "🟠 Average"

    else:
        health = "🔴 Poor"

    # ==========================================
    # METRICS
    # ==========================================

    st.subheader("📊 Dataset Overview")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Rows",
        f"{rows:,}"
    )

    c2.metric(
        "Columns",
        cols
    )

    c3.metric(
        "Missing Values",
        missing
    )

    c4, c5, c6 = st.columns(3)

    c4.metric(
        "Duplicate Rows",
        duplicate
    )

    c5.metric(
        "Quality Score",
        f"{quality}%"
    )

    c6.metric(
        "Dataset Health",
        health
    )

    st.divider()

    # ==========================================
    # DATASET PREVIEW
    # ==========================================

    st.subheader("📄 Dataset Preview")

    st.dataframe(
        df.head(10),
        use_container_width=True
    )

    st.divider()

    st.success("✅ Dashboard Loaded Successfully")