import pandas as pd
import streamlit as st


def calculate_quality_score(df):

    total_cells = df.shape[0] * df.shape[1]

    if total_cells == 0:
        return 0

    missing = df.isnull().sum().sum()
    duplicates = df.duplicated().sum()

    score = 100

    score -= (missing / total_cells) * 100
    score -= (duplicates / df.shape[0]) * 10 if df.shape[0] > 0 else 0

    if score < 0:
        score = 0

    return round(score, 2)


def dataset_profile(df):

    st.subheader("📋 Dataset Profile")

    rows = df.shape[0]
    cols = df.shape[1]

    missing = int(df.isnull().sum().sum())

    duplicates = int(df.duplicated().sum())

    quality = calculate_quality_score(df)

    if quality >= 90:
        status = "🟢 Excellent"

    elif quality >= 75:
        status = "🟡 Good"

    elif quality >= 50:
        status = "🟠 Average"

    else:
        status = "🔴 Poor"

    c1, c2, c3 = st.columns(3)

    c1.metric("Rows", f"{rows:,}")
    c2.metric("Columns", cols)
    c3.metric("Quality Score", f"{quality}%")

    c4, c5, c6 = st.columns(3)

    c4.metric("Missing Values", f"{missing:,}")
    c5.metric("Duplicate Rows", duplicates)
    c6.metric("Health Status", status)

    st.divider()

    st.subheader("📊 Column Information")

    info = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str),
        "Missing": df.isnull().sum().values,
        "Unique": df.nunique().values,
        "Null %": (
            df.isnull().sum().values
            / len(df)
            * 100
        ).round(2)
    })

    st.dataframe(
        info,
        use_container_width=True,
        height=450
    )

    st.divider()

    st.subheader("📈 Statistical Summary")

    st.dataframe(
        df.describe(include="all").fillna(""),
        use_container_width=True
    )