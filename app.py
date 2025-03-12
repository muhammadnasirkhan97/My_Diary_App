# 02
import streamlit as st
import sqlite3
from datetime import date
from modules import task_manager  # Importing task manager module

# --- Database Setup ---
conn = sqlite3.connect("diary.db", check_same_thread=False)
cursor = conn.cursor()

# --- Create Users Table ---
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
""")
conn.commit()

# --- Create Tasks Table ---
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        task_date TEXT,
        task TEXT,
        status TEXT DEFAULT 'Pending'
    )
""")
conn.commit()

# --- Streamlit Session State ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# --- Sidebar Navigation ---
st.sidebar.title("📖 My Diary App")

if st.session_state.logged_in:
    page = st.sidebar.radio("Navigate:", ["🏠 Home", "📝 Task Manager"])
    
    if page == "🏠 Home":
        st.title(f"🏠 Welcome, {st.session_state.user_name}!")
        st.write("Use the sidebar to navigate.")

    elif page == "📝 Task Manager":
        task_manager.show_task_manager()

    # ✅ Fixed Logout Button
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.session_state.user_name = ""
        st.rerun()

    st.stop()  # ✅ Prevents showing login form after logout

# --- Login & Signup UI ---
st.title("📖 My Diary App")

auth_option = st.radio("Select:", ["🔑 Login", "📝 Sign Up"], horizontal=True)

if auth_option == "📝 Sign Up":
    st.subheader("Create a New Account")
    name = st.text_input("👤 Name")
    email = st.text_input("📧 Email")
    password = st.text_input("🔑 Password", type="password")

    if st.button("📝 Sign Up"):
        if name and email and password:
            try:
                cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
                conn.commit()
                st.success("✅ Account Created! Please Login.")
                # ✅ Clear Input Fields
                # st.session_state["signup_name"] = ""
                # st.session_state["signup_email"] = ""
                # st.session_state["signup_password"] = ""

                # st.rerun()  # Refresh the page to reflect the cleared fields

            except sqlite3.IntegrityError:
                st.warning("⚠ Email already exists! Please login.")
        else:
            st.warning("⚠ All fields are required.")

elif auth_option == "🔑 Login":
    st.subheader("Login to Your Account")
    email = st.text_input("📧 Email", key="login_email")
    password = st.text_input("🔑 Password", type="password", key="login_password")

    if st.button("🔓 Login"):
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()
        if user:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.session_state.user_name = user[1]
            st.success(f"✅ Welcome, {user[1]}!")
            st.rerun()  # ✅ Reloads the page to show the Task Manager
        else:
            st.warning("⚠ Invalid email or password!")

# Close DB Connection
conn.close()


#  01
# import streamlit as st
# import sqlite3
# from datetime import date
# from modules  import task_manager 

# # --- Database Setup ---
# conn = sqlite3.connect("diary.db", check_same_thread=False)
# cursor = conn.cursor()

# # --- Create Users Table ---
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT,
#         email TEXT UNIQUE,
#         password TEXT
#     )
# """)
# conn.commit()

# # --- Create Tasks Table ---
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS tasks (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         email TEXT,
#         task_date TEXT,
#         task TEXT,
#         status TEXT DEFAULT 'Pending'
#     )
# """)
# conn.commit()

# # --- Streamlit Session State ---
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False
# if "user_email" not in st.session_state:
#     st.session_state.user_email = ""
# if "user_name" not in st.session_state:
#     st.session_state.user_name = ""

# # --- Sidebar Navigation ---
# st.sidebar.title("📖 My Diary App")

# if st.session_state.logged_in:
#     page = st.sidebar.radio("Navigate:", ["🏠 Home", "📝 Task Manager"])
    
#     if page == "🏠 Home":
#         st.title(f"🏠 Welcome, {st.session_state.user_name}!")
#         st.write("Use the sidebar to navigate.")

#     elif page == "📝 Task Manager":
#         task_manager.show_task_manager()

#     # st.sidebar.button("🚪 Logout", on_click=lambda: (st.session_state.update(logged_in=False), 
#     # st.experimental_rerun()))
#     st.sidebar.button("🚪 Logout", on_click=lambda: (st.session_state.update(logged_in=False), 
#     st.rerun()))
#     st.stop()  # ✅ Prevents showing login form after logout

# # --- Login & Signup UI ---
# st.title("📖 My Diary App")

# auth_option = st.radio("Select:", ["🔑 Login", "📝 Sign Up"], horizontal=True)

# if auth_option == "📝 Sign Up":
#     st.subheader("Create a New Account")
#     name = st.text_input("👤 Name")
#     email = st.text_input("📧 Email")
#     password = st.text_input("🔑 Password", type="password")

#     if st.button("📝 Sign Up"):
#         if name and email and password:
#             try:
#                 cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
#                 conn.commit()
#                 st.success("✅ Account Created! Please Login.")
#             except sqlite3.IntegrityError:
#                 st.warning("⚠ Email already exists! Please login.")
#         else:
#             st.warning("⚠ All fields are required.")

# elif auth_option == "🔑 Login":
#     st.subheader("Login to Your Account")
#     email = st.text_input("📧 Email", key="login_email")
#     password = st.text_input("🔑 Password", type="password", key="login_password")

#     if st.button("🔓 Login"):
#         cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
#         user = cursor.fetchone()
#         if user:
#             st.session_state.logged_in = True
#             st.session_state.user_email = email
#             st.session_state.user_name = user[1]
#             st.success(f"✅ Welcome, {user[1]}!")
#             st.rerun()  # ✅ Reloads the page to show the Task Manager
#         else:
#             st.warning("⚠ Invalid email or password!")

# # Close DB Connection
# conn.close()
