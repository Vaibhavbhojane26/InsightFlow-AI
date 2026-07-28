import pandas as pd
import streamlit as st


def analyze_dataset(df):

    st.subheader("📈 Data Analysis Center")

    numeric_df = df.select_dtypes(include=["number"])

    if numeric_df.empty:
        st.warning("No numeric columns found.")
        return

    st.subheader("📊 Overall Statistics")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Numeric Columns", len(numeric_df.columns))
    c2.metric("Total Records", f"{len(df):,}")
    c3.metric("Total Missing", int(df.isnull().sum().sum()))
    c4.metric("Duplicate Rows", int(df.duplicated().sum()))

    st.divider()

    st.subheader("📋 Statistical Summary")

    st.dataframe(
        numeric_df.describe().round(2),
        use_container_width=True,
        height=350
    )

    st.divider()

    st.subheader("🔗 Correlation Matrix")

    correlation = numeric_df.corr(numeric_only=True)

    st.dataframe(
        correlation.round(2),
        use_container_width=True,
        height=350
    )

    st.divider()

    st.subheader("📌 Missing Values")

    missing = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isnull().sum().values,
        "Missing %": (
            df.isnull().sum().values / len(df) * 100
        ).round(2)
    })

    st.dataframe(
        missing,
        use_container_width=True,
        height=350
    )

    st.divider()

    st.subheader("🎯 Unique Values")

    unique = pd.DataFrame({
        "Column": df.columns,
        "Unique Values": df.nunique().values
    })

    st.dataframe(
        unique,
        use_container_width=True,
        height=350
    )