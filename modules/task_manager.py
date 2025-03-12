import streamlit as st
import sqlite3
from datetime import date

# --- Function to Connect Database ---
def get_db_connection():
    conn = sqlite3.connect("diary.db", check_same_thread=False)
    cursor = conn.cursor()
    return conn, cursor

# --- Function to Show Task Manager ---
def show_task_manager():
    st.title(f"📅 Welcome, {st.session_state.user_name}!")

    # Logout Button
    if st.button("🔓 Logout"):
        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.session_state.user_name = ""
        st.experimental_rerun()
        # st.rerun()

    # Task Input
    task_date = st.date_input("📅 Select Date", date.today())
    task = st.text_area("✍ Write Your Task")

    if st.button("➕ Add Task"):
        if task.strip():
            conn, cursor = get_db_connection()  # Open Connection
            cursor.execute("INSERT INTO tasks (email, task_date, task, status) VALUES (?, ?, ?, ?)", 
                           (st.session_state.user_email, task_date.strftime("%Y-%m-%d"), task, "Pending"))
            conn.commit()
            conn.close()  # Close Connection
            st.success("✅ Task Added Successfully!")
            st.rerun()
        else:
            st.warning("⚠ Task cannot be empty!")

    # Display Tasks
    st.subheader("📜 Your Tasks")
    conn, cursor = get_db_connection()  # Open Connection
    cursor.execute("SELECT id, task_date, task, status FROM tasks WHERE email = ?", (st.session_state.user_email,))
    tasks = cursor.fetchall()
    conn.close()  # Close Connection

    if tasks:
        for task_id, task_date, task_text, status in tasks:
            with st.expander(f"📆 {task_date} - {task_text[:30]}..."):
                st.write(f"📝 {task_text}")
                st.write(f"📌 Status: **{status}**")

                # Mark as Completed
                if st.button(f"✅ Mark as Completed", key=f"complete_{task_id}"):
                    conn, cursor = get_db_connection()
                    cursor.execute("UPDATE tasks SET status = 'Completed' WHERE id = ?", (task_id,))
                    conn.commit()
                    conn.close()
                    st.success("🎉 Task marked as completed!")
                    st.rerun()

                # Delete Task
                if st.button("🗑 Delete Task", key=f"delete_{task_id}"):
                    conn, cursor = get_db_connection()
                    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
                    conn.commit()
                    conn.close()
                    st.warning("🗑 Task deleted!")
                    st.rerun()

    else:
        st.info("ℹ No tasks found! Add a new task.")

