import streamlit as st

from database.database import (
    create_project,
    get_user_projects,
    delete_project
)


# ==========================================
# CREATE NEW PROJECT
# ==========================================

def create_project_ui():

    st.subheader("📁 Create New Project")

    project_name = st.text_input(
        "Project Name",
        key="project_name"
    )

    description = st.text_area(
        "Description",
        key="project_description"
    )

    if st.button(
        "➕ Create Project",
        use_container_width=True
    ):

        if project_name.strip() == "":

            st.warning("Please enter a project name.")

            return

        create_project(

            st.session_state["user_id"],

            project_name,

            description

        )

        st.success("✅ Project Created Successfully")

        st.rerun()


# ==========================================
# PROJECT LIST
# ==========================================

def show_projects():

    st.subheader("📂 My Projects")

    projects = get_user_projects(
        st.session_state["user_id"]
    )

    if len(projects) == 0:

        st.info("No Projects Found")

        return

    for project in projects:

        col1, col2, col3 = st.columns([6,2,1])

        with col1:

            st.write(f"📁 {project['project_name']}")

        with col2:

            if st.button(
                "📂 Open",
                key=f"open_{project['id']}",
                use_container_width=True
            ):

                st.session_state["current_project_id"] = project["id"]

                st.session_state["current_project_name"] = project["project_name"]

                st.success("Project Opened")

                st.rerun()

        with col3:

            if st.button(
                "🗑",
                key=f"delete_{project['id']}",
                use_container_width=True
            ):

                delete_project(project["id"])

                st.success("Project Deleted")

                st.rerun()