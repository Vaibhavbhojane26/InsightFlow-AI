import streamlit as st
import plotly.express as px
import pandas as pd


def visualize_dataset(df):

    st.subheader("📊 Data Visualization Center")

    numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    if len(numeric_columns) == 0:
        st.warning("No numeric columns available.")
        return

    chart = st.selectbox(
        "Select Chart",
        [
            "Histogram",
            "Box Plot",
            "Scatter Plot",
            "Line Chart",
            "Bar Chart",
            "Pie Chart"
        ]
    )

    st.divider()

    if chart == "Histogram":

        column = st.selectbox(
            "Numeric Column",
            numeric_columns
        )

        fig = px.histogram(
            df,
            x=column,
            title=f"{column} Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

    elif chart == "Box Plot":

        column = st.selectbox(
            "Numeric Column",
            numeric_columns
        )

        fig = px.box(
            df,
            y=column,
            title=f"{column} Box Plot"
        )

        st.plotly_chart(fig, use_container_width=True)

    elif chart == "Scatter Plot":

        if len(numeric_columns) < 2:

            st.warning("Minimum 2 numeric columns required.")

        else:

            x = st.selectbox(
                "X Axis",
                numeric_columns
            )

            y = st.selectbox(
                "Y Axis",
                numeric_columns,
                index=1
            )

            fig = px.scatter(
                df,
                x=x,
                y=y,
                title=f"{x} vs {y}"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    elif chart == "Line Chart":

        x = st.selectbox(
            "X Axis",
            df.columns
        )

        y = st.selectbox(
            "Y Axis",
            numeric_columns
        )

        fig = px.line(
            df,
            x=x,
            y=y,
            title=f"{y} Trend"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    elif chart == "Bar Chart":

        if len(categorical_columns) == 0:

            st.warning("No categorical columns found.")

        else:

            column = st.selectbox(
                "Category",
                categorical_columns
            )

            data = (
                df[column]
                .value_counts()
                .reset_index()
            )

            data.columns = [column, "Count"]

            fig = px.bar(
                data,
                x=column,
                y="Count",
                title=f"{column} Distribution"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    elif chart == "Pie Chart":

        if len(categorical_columns) == 0:

            st.warning("No categorical columns found.")

        else:

            column = st.selectbox(
                "Category",
                categorical_columns
            )

            data = (
                df[column]
                .value_counts()
                .reset_index()
            )

            data.columns = [column, "Count"]

            fig = px.pie(
                data,
                names=column,
                values="Count",
                title=f"{column} Distribution"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )