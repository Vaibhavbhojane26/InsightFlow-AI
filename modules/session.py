import streamlit as st


# ==========================================
# LOGIN SESSION
# ==========================================

def login(user):

    st.session_state["login"] = True
    st.session_state["user_id"] = user["id"]
    st.session_state["user_name"] = user["full_name"]
    st.session_state["email"] = user["email"]


# ==========================================
# LOGOUT SESSION
# ==========================================

def logout():

    keys = list(st.session_state.keys())

    for key in keys:
        del st.session_state[key]


# ==========================================
# CURRENT USER
# ==========================================

def current_user():

    return {

        "id": st.session_state.get("user_id"),

        "name": st.session_state.get("user_name"),

        "email": st.session_state.get("email")

    }


# ==========================================
# LOGIN STATUS
# ==========================================

def is_logged_in():

    return st.session_state.get(
        "login",
        False
    )


# ==========================================
# CURRENT PROJECT
# ==========================================

def open_project(project):

    st.session_state["current_project_id"] = project["id"]

    st.session_state["current_project_name"] = project["project_name"]


# ==========================================
# GET CURRENT PROJECT
# ==========================================

def current_project():

    return {

        "id": st.session_state.get(
            "current_project_id"
        ),

        "name": st.session_state.get(
            "current_project_name"
        )

    }


# ==========================================
# PROJECT OPEN ?
# ==========================================

def project_open():

    return "current_project_id" in st.session_state