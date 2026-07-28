import pandas as pd
import streamlit as st


def clean_dataset(df):

    st.subheader("🧹 Data Cleaning Center")

    cleaned_df = df.copy()

    c1, c2 = st.columns(2)

    with c1:

        if st.button("🗑 Remove Duplicate Rows", use_container_width=True):

            before = len(cleaned_df)

            cleaned_df = cleaned_df.drop_duplicates()

            removed = before - len(cleaned_df)

            st.success(f"✅ {removed} duplicate rows removed.")

    with c2:

        if st.button("❌ Remove Empty Rows", use_container_width=True):

            before = len(cleaned_df)

            cleaned_df = cleaned_df.dropna(how="all")

            removed = before - len(cleaned_df)

            st.success(f"✅ {removed} empty rows removed.")

    st.divider()

    st.subheader("📌 Missing Value Handling")

    numeric_columns = cleaned_df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    categorical_columns = cleaned_df.select_dtypes(
        include=["object"]
    ).columns.tolist()

    col1, col2 = st.columns(2)

    with col1:

        if st.button("Fill Numeric Missing Values", use_container_width=True):

            for column in numeric_columns:

                cleaned_df[column] = cleaned_df[column].fillna(
                    cleaned_df[column].median()
                )

            st.success("✅ Numeric missing values filled.")

    with col2:

        if st.button("Fill Text Missing Values", use_container_width=True):

            for column in categorical_columns:

                mode = cleaned_df[column].mode()

                if not mode.empty:

                    cleaned_df[column] = cleaned_df[column].fillna(mode[0])

            st.success("✅ Text missing values filled.")

    st.divider()

    st.subheader("👀 Cleaned Dataset")

    st.dataframe(
        cleaned_df,
        use_container_width=True,
        height=450
    )

    csv = cleaned_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download Clean Dataset",
        csv,
        "cleaned_dataset.csv",
        "text/csv",
        use_container_width=True
    )

    return cleaned_df