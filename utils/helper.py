import pandas as pd
import numpy as np


def data_quality_score(df):

    total_cells = df.shape[0] * df.shape[1]

    missing = df.isnull().sum().sum()

    duplicates = df.duplicated().sum()

    score = 100

    if total_cells > 0:
        score -= (missing / total_cells) * 100

    if len(df) > 0:
        score -= (duplicates / len(df)) * 20

    if score < 0:
        score = 0

    return round(score, 2)


def missing_summary(df):

    return pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isnull().sum().values,
        "Percentage": (
            df.isnull().sum() / len(df) * 100
        ).round(2)
    })


def duplicate_count(df):

    return int(df.duplicated().sum())


def numeric_columns(df):

    return df.select_dtypes(
        include=np.number
    ).columns.tolist()


def categorical_columns(df):

    return df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()


def datetime_columns(df):

    return df.select_dtypes(
        include=["datetime64"]
    ).columns.tolist()


def file_size(uploaded_file):

    size = uploaded_file.size / (1024 * 1024)

    return round(size, 2)


def dataset_shape(df):

    return df.shape[0], df.shape[1]