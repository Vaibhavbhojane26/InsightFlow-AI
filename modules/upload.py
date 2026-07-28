
import os
import zipfile
from datetime import datetime

import pandas as pd
import streamlit as st

from config import (
    UPLOAD_FOLDER,
    SUPPORTED_FILES
)


# ===========================================
# CREATE UPLOAD FOLDER
# ===========================================

def create_upload_folder():

    os.makedirs(
        UPLOAD_FOLDER,
        exist_ok=True
    )


# ===========================================
# FILE SIZE
# ===========================================

def get_file_size(size):

    units = ["Bytes", "KB", "MB", "GB", "TB"]

    index = 0

    while size >= 1024 and index < len(units)-1:

        size /= 1024

        index += 1

    return f"{round(size,2)} {units[index]}"


# ===========================================
# AUTO CSV READER
# ===========================================

def read_csv_file(file_path):

    encodings = [

        "utf-8",

        "utf-8-sig",

        "latin1",

        "cp1252",

        "ISO-8859-1",

        "utf-16"

    ]

    separators = [

        ",",

        ";",

        "\t",

        "|"

    ]

    last_error = None

    for encoding in encodings:

        for separator in separators:

            try:

                df = pd.read_csv(

                    file_path,

                    encoding=encoding,

                    sep=separator,

                    low_memory=False

                )

                if len(df.columns) > 1:

                    return df

            except Exception as e:

                last_error = e

    raise last_error


# ===========================================
# UNIVERSAL DATA LOADER
# ===========================================

def load_dataset(file_path):

    extension = os.path.splitext(
        file_path
    )[1].lower()

    # CSV

    if extension == ".csv":

        return read_csv_file(file_path)

    # TSV

    elif extension == ".tsv":

        return pd.read_csv(
            file_path,
            sep="\t"
        )

    # Excel

    elif extension in [".xlsx", ".xls"]:

        excel = pd.ExcelFile(
            file_path,
            engine="openpyxl"
        )

        sheet = excel.sheet_names[0]

        return pd.read_excel(

            file_path,

            sheet_name=sheet,

            engine="openpyxl"

        )

    # JSON

    elif extension == ".json":

        return pd.read_json(file_path)

    # Parquet

    elif extension == ".parquet":

        return pd.read_parquet(file_path)

    # Feather

    elif extension == ".feather":

        return pd.read_feather(file_path)

    # Pickle

    elif extension == ".pkl":

        return pd.read_pickle(file_path)

    # XML

    elif extension == ".xml":

        return pd.read_xml(file_path)

    # HTML Table

    elif extension in [

        ".html",

        ".htm"

    ]:

        return pd.read_html(file_path)[0]

    # ODS

    elif extension == ".ods":

        return pd.read_excel(
            file_path,
            engine="odf"
        )

    # ZIP

    elif extension == ".zip":

        with zipfile.ZipFile(file_path) as z:

            z.extractall(
                UPLOAD_FOLDER
            )

            for file in z.namelist():

                extracted = os.path.join(

                    UPLOAD_FOLDER,

                    file

                )

                return load_dataset(
                    extracted
                )

    else:

        raise Exception(

            f"Unsupported file format : {extension}"

        )
    

# ===========================================
# UPLOAD DATASET
# ===========================================

def upload_dataset():

    create_upload_folder()

    uploaded_file = st.file_uploader(
        "📂 Upload Dataset",
        type=SUPPORTED_FILES
    )

    if uploaded_file is None:
        return None

    file_path = os.path.join(
        UPLOAD_FOLDER,
        uploaded_file.name
    )

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    try:

        df = load_dataset(file_path)

    except Exception as e:

        st.error(
            f"❌ Unable to read file.\n\n{e}"
        )

        return None

    st.success("✅ Dataset Uploaded Successfully")
   

    st.divider()

    st.subheader("📄 Dataset Information")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "File Name",
        uploaded_file.name
    )

    c2.metric(
        "File Type",
        os.path.splitext(
            uploaded_file.name
        )[1].upper()
    )

    c3.metric(
        "File Size",
        get_file_size(
            uploaded_file.size
        )
    )

    c4.metric(
        "Uploaded",
        datetime.now().strftime("%H:%M:%S")
    )

    st.divider()

    c5, c6, c7, c8 = st.columns(4)

    c5.metric(
        "Rows",
        f"{df.shape[0]:,}"
    )

    c6.metric(
        "Columns",
        df.shape[1]
    )

    memory = round(

        df.memory_usage(
            deep=True
        ).sum()

        /1024/1024,

        2

    )

    c7.metric(
        "Memory",
        f"{memory} MB"
    )

    c8.metric(
        "Missing",
        int(
            df.isnull().sum().sum()
        )
    )

    st.divider()

    st.subheader("👀 Dataset Preview")

    st.dataframe(

        df,

        use_container_width=True,

        height=500

    )

    return df