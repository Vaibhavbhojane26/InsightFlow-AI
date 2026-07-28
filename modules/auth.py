import re
import hashlib
import streamlit as st

from database.database import (
    get_user,
    add_user,
    save_login,
    save_activity
)

# ==========================================
# PASSWORD HASHING
# ==========================================

def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


# ==========================================
# EMAIL VALIDATION
# ==========================================

def valid_email(email):

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    return re.match(
        pattern,
        email
    )


# ==========================================
# PASSWORD VALIDATION
# ==========================================

def valid_password(password):

    if len(password) < 8:

        return False

    return True


# ==========================================
# REGISTER USER
# ==========================================

def register_user(

    full_name,

    email,

    mobile,

    password,

    confirm_password

):

    if full_name.strip() == "":

        return False, "Full Name Required"

    if not valid_email(email):

        return False, "Invalid Email"

    if not valid_password(password):

        return False, "Password must contain minimum 8 characters"

    if password != confirm_password:

        return False, "Passwords do not match"

    user = get_user(email)

    if user:

        return False, "Email already exists"

    password_hash = hash_password(password)

    add_user(

        full_name,

        email,

        mobile,

        password_hash

    )

    return True, "Registration Successful"


# ==========================================
# LOGIN USER
# ==========================================

def login_user(

    email,

    password

):

    user = get_user(email)

    if user is None:

        return False

    password_hash = hash_password(password)

    if user["password_hash"] != password_hash:

        return False

    save_login(user["id"])

    save_activity(

        user["id"],

        "User Login"

    )

    st.session_state["login"] = True

    st.session_state["user_id"] = user["id"]

    st.session_state["user_name"] = user["full_name"]

    st.session_state["email"] = user["email"]

    return True
# ==========================================
# LOGIN PAGE
# ==========================================

def login_page():

    st.title("🔐 Login")

    st.caption("Welcome to InsightFlow AI")

    email = st.text_input(
        "Email",
        key="login_email"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )

    if st.button(
        "🔑 Login",
        use_container_width=True
    ):

        success = login_user(
            email,
            password
        )

        if success:

            st.success("Login Successful")

            st.rerun()

        else:

            st.error("Invalid Email or Password")


# ==========================================
# REGISTER PAGE
# ==========================================

def register_page():

    st.title("📝 Create Account")

    full_name = st.text_input(
        "Full Name",
        key="register_name"
    )

    email = st.text_input(
        "Email Address",
        key="register_email"
    )

    mobile = st.text_input(
        "Mobile Number",
        key="register_mobile"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="register_password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        key="register_confirm_password"
    )

    if st.button(
        "✅ Register",
        use_container_width=True
    ):

        success, message = register_user(
            full_name,
            email,
            mobile,
            password,
            confirm_password
        )

        if success:

            st.success(message)

        else:

            st.error(message)

# ==========================================
# LOGOUT
# ==========================================

def logout():

    if "user_id" in st.session_state:

        save_activity(
            st.session_state["user_id"],
            "User Logout"
        )

    keys = list(st.session_state.keys())

    for key in keys:

        del st.session_state[key]

    st.success(
        "Logged Out Successfully"
    )

    st.rerun()


# ==========================================
# SESSION INITIALIZATION
# ==========================================

def initialize_session():

    if "login" not in st.session_state:

        st.session_state["login"] = False

    if "user_id" not in st.session_state:

        st.session_state["user_id"] = None

    if "user_name" not in st.session_state:

        st.session_state["user_name"] = ""

    if "email" not in st.session_state:

        st.session_state["email"] = ""


# ==========================================
# LOGIN CHECK
# ==========================================

def is_logged_in():

    return st.session_state.get(
        "login",
        False
    )


# ==========================================
# USER PROFILE
# ==========================================

def user_profile():

    with st.sidebar:

        st.divider()

        st.subheader("👤 User")

        st.write(
            st.session_state.get(
                "user_name",
                "Guest"
            )
        )

        st.caption(
            st.session_state.get(
                "email",
                ""
            )
        )

        st.success("🟢 Online")

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            logout()


# ==========================================
# LOGIN REQUIRED
# ==========================================

def login_required():

    initialize_session()

    if not is_logged_in():

        tab1, tab2 = st.tabs(
            [
                "🔐 Login",
                "📝 Register"
            ]
        )

        with tab1:

            login_page()

        with tab2:

            register_page()

        st.stop()

    user_profile()
    # ==========================================
# ADMIN ROLE CHECK
# ==========================================

def is_admin():

    role = st.session_state.get(
        "role",
        "user"
    )

    return role.lower() == "admin"


# ==========================================
# ADMIN ACCESS
# ==========================================

def admin_required():

    if not is_admin():

        st.error(
            "⛔ Admin access required."
        )

        st.stop()


# ==========================================
# USER GREETING
# ==========================================

def welcome_user():

    name = st.session_state.get(
        "user_name",
        "User"
    )

    st.success(
        f"👋 Welcome, {name}"
    )


# ==========================================
# CURRENT USER
# ==========================================

def current_user():

    return {

        "id": st.session_state.get(
            "user_id"
        ),

        "name": st.session_state.get(
            "user_name"
        ),

        "email": st.session_state.get(
            "email"
        )

    }


# ==========================================
# SESSION RESET
# ==========================================

def reset_session():

    st.session_state["login"] = False

    st.session_state["user_id"] = None

    st.session_state["user_name"] = ""

    st.session_state["email"] = ""


# ==========================================
# AUTH INITIALIZATION
# ==========================================

def initialize_auth():

    initialize_session()

    login_required()