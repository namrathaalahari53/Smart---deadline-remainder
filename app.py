import streamlit as st
from datetime import date

st.set_page_config(
    page_title="Smart Deadline Reminder",
    page_icon="📅",
    layout="wide"
)

# Initialize tasks
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Sidebar menu
st.sidebar.title("📅 Smart Deadline Reminder")
st.sidebar.write("Manage your tasks easily")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Add Tasks", "My Tasks", "Task Summary"]
)

st.sidebar.markdown("---")
st.sidebar.caption("Stay organized. Meet every deadline!")

# Dashboard
if page == "Dashboard":
    st.title("🏠 Dashboard")
    st.write("Welcome to Smart Deadline Reminder!")
    st.write("Manage your tasks and never miss a deadline.")

    total = len(st.session_state.tasks)
    completed = sum(
        1 for task in st.session_state.tasks
        if task["completed"]
    )
    pending = total - completed

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Tasks", total)
    col2.metric("Completed", completed)
    col3.metric("Pending", pending)

    st.info("Use the menu on the left to manage your tasks.")

# Add Tasks
elif page == "Add Tasks":
    st.title("➕ Add a New Task")

    with st.form("add_task_form"):
        task_name = st.text_input("Task Name")
        deadline = st.date_input(
            "Deadline",
            value=date.today()
        )

        submitted = st.form_submit_button("Add Task")

        if submitted:
            if task_name.strip():
                st.session_state.tasks.append({
                    "name": task_name.strip(),
                    "deadline": deadline,
                    "completed": False
                })
                st.success(
                    f"Task '{task_name.strip()}' added successfully!"
                )
            else:
                st.error("Please enter a task name!")

# My Tasks
elif page == "My Tasks":
    st.title("📋 My Tasks")

    if not st.session_state.tasks:
        st.info("No tasks yet. Go to Add Tasks to create one.")
    else:
        for i, task in enumerate(st.session_state.tasks):
            with st.container(border=True):
                col1, col2, col3 = st.columns([3, 2, 2])

                col1.write(f"**{task['name']}**")
                col2.write(f"📅 {task['deadline']}")

                if task["completed"]:
                    col3.success("Completed")
                else:
                    col3.warning("Pending")

                action1, action2 = st.columns(2)

                if not task["completed"]:
                    if action1.button(
                        "Mark as Complete",
                        key=f"complete_{i}"
                    ):
                        st.session_state.tasks[i]["completed"] = True
                        st.rerun()

                if action2.button("Delete", key=f"delete_{i}"):
                    st.session_state.tasks.pop(i)
                    st.rerun()

# Task Summary
elif page == "Task Summary":
    st.title("📊 Task Summary")

    total = len(st.session_state.tasks)
    completed = sum(
        1 for task in st.session_state.tasks
        if task["completed"]
    )
    pending = total - completed

    st.metric("Total Tasks", total)
    st.metric("Completed Tasks", completed)
    st.metric("Pending Tasks", pending)

    if total > 0:
        progress = completed / total
        st.write("Completion Progress")
        st.progress(progress)
        st.write(f"{int(progress * 100)}% completed")
    else:
        st.info("Add some tasks to see your summary.")
