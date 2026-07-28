from io import BytesIO

import pandas as pd
import streamlit as st


# ==========================================
# DOWNLOAD CSV
# ==========================================

def download_csv(df):

    csv = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇ Download CSV",
        data=csv,
        file_name="cleaned_dataset.csv",
        mime="text/csv",
        use_container_width=True
    )


# ==========================================
# DOWNLOAD EXCEL
# ==========================================

def download_excel(df):

    output = BytesIO()

    try:

        with pd.ExcelWriter(
            output,
            engine="xlsxwriter"
        ) as writer:

            df.to_excel(
                writer,
                index=False,
                sheet_name="Dataset"
            )

        output.seek(0)

        st.download_button(
            label="⬇ Download Excel",
            data=output,
            file_name="cleaned_dataset.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    except Exception as e:

        st.error(
            f"Excel Export Error:\n\n{e}"
        )


# ==========================================
# DATASET PREVIEW
# ==========================================

def preview_dataset(df):

    st.subheader("👀 Dataset Preview")

    st.dataframe(
        df,
        use_container_width=True,
        height=500
    )


# ==========================================
# DATASET INFORMATION
# ==========================================

def dataset_information(df):

    st.subheader("📄 Dataset Information")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Rows",
        f"{df.shape[0]:,}"
    )

    c2.metric(
        "Columns",
        df.shape[1]
    )

    memory = round(
        df.memory_usage(deep=True).sum() / 1024 / 1024,
        2
    )

    c3.metric(
        "Memory",
        f"{memory} MB"
    )

    c4.metric(
        "Missing Values",
        int(df.isnull().sum().sum())
    )

    st.divider()