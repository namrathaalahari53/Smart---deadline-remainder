import streamlit as st
from datetime import date

st.set_page_config(
    page_title="Smart Deadline Reminder",
    page_icon="⏰",
    layout="centered"
)

# Initialize tasks
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Initialize message
if "success_message" not in st.session_state:
    st.session_state.success_message = ""

st.title("⏰ Smart Deadline Reminder")
st.write("Manage your tasks and never miss a deadline!")

st.divider()

# Add New Task
st.header("➕ Add a New Task")

with st.form("task_form", clear_on_submit=True):
    task_name = st.text_input(
        "Task Name",
        placeholder="Enter your task name"
    )

    deadline = st.date_input(
        "Select Deadline",
        value=date.today()
    )

    submitted = st.form_submit_button(
        "Add Task",
        use_container_width=True
    )

if submitted:
    if task_name.strip():
        st.session_state.tasks.append({
            "name": task_name.strip(),
            "deadline": deadline,
            "completed": False
        })

        st.session_state.success_message = (
            f"Task '{task_name.strip()}' added successfully! 🎉"
        )
    else:
        st.session_state.success_message = ""
        st.error("Please enter a task name!")

# Show success message
if st.session_state.success_message:
    st.success(st.session_state.success_message)
    st.session_state.success_message = ""

st.divider()

# My Tasks
st.header("📋 My Tasks")

if not st.session_state.tasks:
    st.info("No tasks added yet. Add your first task!")
else:
    for i, task in enumerate(st.session_state.tasks):
        with st.container(border=True):
            st.subheader(task["name"])

            st.write(
                "📅 Deadline: "
                + task["deadline"].strftime("%d-%m-%Y")
            )

            if task["completed"]:
                st.success("✅ Task Completed")
            elif task["deadline"] < date.today():
                st.error("⚠️ Deadline has passed!")
            elif task["deadline"] == date.today():
                st.warning("⏰ Deadline is today!")
            else:
                st.info("🕒 Task Pending")

            col1, col2 = st.columns(2)

            with col1:
                if not task["completed"]:
                    if st.button(
                        "Mark as Complete",
                        key=f"complete_{i}",
                        use_container_width=True
                    ):
                        st.session_state.tasks[i]["completed"] = True
                        st.rerun()

            with col2:
                if st.button(
                    "Delete Task",
                    key=f"delete_{i}",
                    use_container_width=True
                ):
                    st.session_state.tasks.pop(i)
                    st.rerun()

st.divider()

# Task Summary
st.header("📊 Task Summary")

total_tasks = len(st.session_state.tasks)
completed_tasks = sum(
    task["completed"] for task in st.session_state.tasks
)
pending_tasks = total_tasks - completed_tasks

col1, col2, col3 = st.columns(3)

col1.metric("Total Tasks", total_tasks)
col2.metric("Completed", completed_tasks)
col3.metric("Pending", pending_tasks)

st.divider()

st.caption(
    "Smart Deadline Reminder | Stay organized and meet your deadlines!"
)
