import pandas as pd
import streamlit as st


def generate_insights(df):

    st.subheader("💡 AI Business Insights")

    insights = []

    # Dataset Overview
    insights.append(
        f"📊 Dataset contains {df.shape[0]:,} rows and {df.shape[1]} columns."
    )

    # Missing Values
    missing = int(df.isnull().sum().sum())

    if missing == 0:
        insights.append("✅ Dataset has no missing values.")
    else:
        insights.append(f"⚠ Dataset contains {missing:,} missing values.")

    # Duplicate Rows
    duplicate = int(df.duplicated().sum())

    if duplicate == 0:
        insights.append("✅ No duplicate rows detected.")
    else:
        insights.append(f"⚠ {duplicate} duplicate rows detected.")

    # Numeric Insights
    numeric_columns = df.select_dtypes(include=["number"]).columns

    for column in numeric_columns:

        insights.append(
            f"📈 {column} Average : {df[column].mean():.2f}"
        )

        insights.append(
            f"🔺 Highest {column} : {df[column].max()}"
        )

        insights.append(
            f"🔻 Lowest {column} : {df[column].min()}"
        )

        if df[column].isnull().sum() > 0:

            insights.append(
                f"⚠ {column} contains {df[column].isnull().sum()} missing values."
            )

    # Categorical Insights
    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns

    for column in categorical_columns:

        mode = df[column].mode()

        if not mode.empty:

            insights.append(
                f"🏆 Most frequent value in '{column}' : {mode[0]}"
            )

        insights.append(
            f"📌 '{column}' has {df[column].nunique()} unique values."
        )

    # Display Insights
    st.subheader("📋 Generated Insights")

    for insight in insights:
        st.success(insight)

    # Recommendations
    st.divider()

    st.subheader("🎯 Recommendations")

    if missing > 0:
        st.warning("Clean missing values before building ML models.")

    if duplicate > 0:
        st.warning("Remove duplicate rows for better accuracy.")

    if missing == 0 and duplicate == 0:
        st.success("Dataset looks clean and ready for further analysis.")

    return insights