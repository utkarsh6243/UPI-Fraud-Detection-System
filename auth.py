import streamlit as st
import sqlite3
import hashlib

DATABASE = "transactions.db"


# ---------------- PASSWORD HASH ---------------- #

def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


# ---------------- DATABASE ---------------- #

def get_connection():

    return sqlite3.connect(DATABASE)


# ---------------- USERS TABLE ---------------- #

def create_user_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        username TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        role TEXT DEFAULT 'User',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    conn.commit()

    conn.close()


# ---------------- DEFAULT ADMIN ---------------- #

def create_admin():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM users WHERE username=?",

        ("admin",)

    )

    if cursor.fetchone() is None:

        cursor.execute("""

        INSERT INTO users(

            name,

            username,

            password,

            role

        )

        VALUES(?,?,?,?)

        """,

        (

            "Administrator",

            "admin",

            hash_password("admin123"),

            "Admin"

        )

        )

        conn.commit()

    conn.close()


create_user_table()
create_admin()
# ---------------- LOGIN ---------------- #

def login():

    if "logged_in" not in st.session_state:

        st.session_state.logged_in = False

    if st.session_state.logged_in:

        return True

    st.markdown("""

    <style>

    .login-box{

        background:rgba(15,23,42,.88);

        border:1px solid rgba(255,255,255,.08);

        border-radius:20px;

        padding:35px;

        box-shadow:0px 15px 35px rgba(0,0,0,.35);

    }

    .heading{

        text-align:center;

        color:#38BDF8;

        font-size:34px;

        font-weight:bold;

    }

    .sub{

        text-align:center;

        color:#94A3B8;

        font-size:14px;

        margin-bottom:20px;

    }

    </style>

    """, unsafe_allow_html=True)

    left, center, right = st.columns([1,2,1])

    with center:

        st.markdown('<div class="heading">🛡 UPI AI Shield</div>', unsafe_allow_html=True)

        st.markdown('<div class="sub">Enterprise Fraud Detection Platform</div>', unsafe_allow_html=True)

        login_tab, signup_tab = st.tabs(

            [

                "🔐 Login",

                "👤 Create Account"

            ]

        )

        # ================= LOGIN ================= #

        with login_tab:

            username = st.text_input(

                "Username",

                key="login_username"

            )

            password = st.text_input(

                "Password",

                type="password",

                key="login_password"

            )

            if st.button(

                "Secure Login",

                use_container_width=True,

                type="primary"

            ):

                conn = get_connection()

                cursor = conn.cursor()

                cursor.execute(

                    """

                    SELECT *

                    FROM users

                    WHERE username=?

                    AND password=?

                    """,

                    (

                        username,

                        hash_password(password)

                    )

                )

                user = cursor.fetchone()

                conn.close()

                if user:

                    st.session_state.logged_in = True

                    st.session_state.name = user[1]

                    st.session_state.role = user[4]

                    st.success("Login Successful")

                    st.rerun()

                else:

                    st.error("Invalid Username or Password")
                            # ================= CREATE ACCOUNT ================= #

        with signup_tab:

            st.subheader("Create New Account")

            full_name = st.text_input(
                "Full Name",
                key="signup_name"
            )

            username = st.text_input(
                "Username",
                key="signup_username"
            )

            password = st.text_input(
                "Password",
                type="password",
                key="signup_password"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                key="signup_confirm"
            )

            role = st.selectbox(
                "Role",
                [
                    "User",
                    "Admin"
                ],
                key="signup_role"
            )

            if st.button(
                "Create Account",
                use_container_width=True
            ):

                if full_name.strip() == "" or username.strip() == "" or password.strip() == "":

                    st.error("Please fill all fields.")

                elif password != confirm_password:

                    st.error("Passwords do not match.")

                elif len(password) < 6:

                    st.error("Password must contain at least 6 characters.")

                else:

                    conn = get_connection()

                    cursor = conn.cursor()

                    cursor.execute(

                        "SELECT * FROM users WHERE username=?",

                        (username,)

                    )

                    existing = cursor.fetchone()

                    if existing:

                        st.error("Username already exists.")

                    else:

                        cursor.execute(

                            """

                            INSERT INTO users
                            (
                                name,
                                username,
                                password,
                                role
                            )

                            VALUES
                            (
                                ?,
                                ?,
                                ?,
                                ?
                            )

                            """,

                            (

                                full_name,

                                username,

                                hash_password(password),

                                role

                            )

                        )

                        conn.commit()

                        conn.close()

                        st.success("🎉 Account created successfully!")

                        st.info(
                            "You can now log in using your username and password."
                        )

    return False
# ---------------- LOGOUT ---------------- #

def logout():

    if st.sidebar.button(
        "Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False

        st.session_state.clear()

        st.rerun()