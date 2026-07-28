import streamlit as st
import pandas as pd
import os

from database.database import (
    get_project_files,
    get_dataset_by_id
)

from modules.upload import upload_dataset


# ==========================================
# PROJECT WORKSPACE
# ==========================================

def project_workspace():

    if "current_project_id" not in st.session_state:
        st.warning("Please open a project first.")
        return

    if st.button(
        "⬅ Back to Projects",
        key="workspace_back_button"
    ):
        st.session_state.pop("current_project_id", None)
        st.session_state.pop("current_project_name", None)
        st.rerun()

    st.title(f"📁 {st.session_state['current_project_name']}")
    st.caption("Project Workspace")

    st.divider()

    st.subheader("📤 Upload Dataset")

    df = upload_dataset()

    if df is not None:
        st.session_state.dataset = df

    st.divider()

    st.subheader("📂 Uploaded Files")

    files = get_project_files(
        st.session_state["current_project_id"]
    )

    if len(files) == 0:

        st.info("No files uploaded yet.")

    else:

        for file in files:

            col1, col2 = st.columns([8,2])

            with col1:

                st.write(f"📄 {file['file_name']}")

            with col2:

                if st.button(
                    "📂 Open",
                    key=f"open_{file['id']}"
                ):

                    path = file["file_path"]

                    if not os.path.exists(path):

                        st.error("File not found.")

                    else:

                        extension = os.path.splitext(path)[1].lower()

                        try:

                            if extension == ".csv":

                                dataset = pd.read_csv(path)

                            else:

                                dataset = pd.read_excel(path)

                            st.session_state.dataset = dataset

                            st.success("✅ File Opened Successfully")

                            st.rerun()

                        except Exception as e:

                            st.error(e)

    if st.session_state.get("dataset") is not None:

        st.divider()

        st.subheader("👀 Dataset Preview")

        st.dataframe(
            st.session_state.dataset,
            use_container_width=True,
            height=400
        )