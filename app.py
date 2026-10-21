
import streamlit as st
import json
import os
import csv
import io
from datetime import date

st.set_page_config(
    page_title="Smart Deadline Reminder",
    page_icon="⏰",
    layout="wide"
)

FILE_NAME = "tasks.json"

# Professional styling
st.markdown("""
<style>
    .main {
        background-color: #f5f7fb;
    }
    h1 {
        color: #2446a6;
    }
    div[data-testid="stMetric"] {
        background: white;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #e3e8f2;
    }
    div.stButton > button {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)


def load_tasks():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                tasks = json.load(file)

            for task in tasks:
                task["deadline"] = date.fromisoformat(
                    task["deadline"]
                )
            return tasks
        except (json.JSONDecodeError, ValueError, KeyError):
            return []
    return []


def save_tasks():
    with open(FILE_NAME, "w") as file:
        json.dump(
            st.session_state.tasks,
            file,
            default=str,
            indent=4
        )


if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

tasks = st.session_state.tasks

# Sidebar navigation
st.sidebar.title("⏰ Deadline Manager")
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Add Task", "My Tasks", "Downloads"]
)

st.sidebar.divider()
st.sidebar.caption("Stay organized. Meet every deadline!")

# Main title
st.title("⏰ Smart Deadline Reminder")
st.write("Manage your tasks, track deadlines, and improve productivity.")

# Dashboard
if page == "Dashboard":
    st.header("📊 Dashboard")

    total = len(tasks)
    completed = sum(1 for task in tasks if task["completed"])
    pending = total - completed
    overdue = sum(
        1 for task in tasks
        if not task["completed"]
        and task["deadline"] < date.today()
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Tasks", total)
    c2.metric("Completed", completed)
    c3.metric("Pending", pending)
    c4.metric("Overdue", overdue)

    st.subheader("📈 Completion Progress")
    progress = completed / total if total else 0
    st.progress(progress)
    st.write(f"{progress * 100:.0f}% of tasks completed")

    st.divider()
    st.subheader("⏰ Deadline Reminders")

    reminders = [
        task for task in tasks
        if not task["completed"]
        and (task["deadline"] - date.today()).days <= 2
    ]

    if reminders:
        for task in reminders:
            days = (task["deadline"] - date.today()).days
            if days < 0:
                st.error(f'Overdue: {task["name"]}')
            elif days == 0:
                st.warning(f'Due today: {task["name"]}')
            else:
                st.warning(
                    f'{task["name"]}: due in {days} day(s)'
                )
    else:
        st.success("No urgent deadlines right now!")

    if not tasks:
        st.info("Start by adding your first task from the sidebar.")

# Add task
elif page == "Add Task":
    st.header("➕ Add a New Task")

    with st.form("task_form"):
        name = st.text_input("Task name")
        deadline = st.date_input(
            "Deadline",
            min_value=date.today()
        )
        priority = st.selectbox(
            "Priority",
            ["High", "Medium", "Low"]
        )
        submitted = st.form_submit_button("Add Task")

    if submitted:
        if name.strip():
            tasks.append({
                "name": name.strip(),
                "deadline": deadline,
                "priority": priority,
                "completed": False
            })
            save_tasks()
            st.success("Task added successfully!")
            st.rerun()
        else:
            st.warning("Please enter a task name.")

# My tasks
elif page == "My Tasks":
    st.header("📋 My Tasks")

    search = st.text_input("🔍 Search by task name")
    status_filter = st.selectbox(
        "Filter by status",
        ["All Tasks", "Pending Tasks", "Completed Tasks"]
    )

    filtered = []
    for index, task in enumerate(tasks):
        matches_search = search.lower() in task["name"].lower()

        if status_filter == "Pending Tasks":
            matches_status = not task["completed"]
        elif status_filter == "Completed Tasks":
            matches_status = task["completed"]
        else:
            matches_status = True

        if matches_search and matches_status:
            filtered.append((index, task))

    if not filtered:
        st.info("No matching tasks found.")

    for index, task in filtered:
        with st.container(border=True):
            st.subheader(task["name"])
            st.write("📅 Deadline:", task["deadline"])

            priority_icons = {
                "High": "🔴",
                "Medium": "🟡",
                "Low": "🟢"
            }
            st.write(
                f'{priority_icons.get(task["priority"], "⚪")} '
                f'Priority: {task["priority"]}'
            )

            if task["completed"]:
                st.success("Completed ✅")
            else:
                days_left = (task["deadline"] - date.today()).days
                if days_left < 0:
                    st.error("Deadline missed!")
                elif days_left == 0:
                    st.warning("Deadline is today!")
                else:
                    st.info(f"{days_left} day(s) remaining")

            with st.expander("✏️ Edit Task"):
                with st.form(f"edit_{index}"):
                    new_name = st.text_input(
                        "Task name",
                        value=task["name"],
                        key=f"name_{index}"
                    )
                    new_deadline = st.date_input(
                        "Deadline",
                        value=task["deadline"],
                        key=f"date_{index}"
                    )
                    new_priority = st.selectbox(
                        "Priority",
                        ["High", "Medium", "Low"],
                        index=["High", "Medium", "Low"].index(
                            task["priority"]
                        ),
                        key=f"priority_{index}"
                    )
                    edit = st.form_submit_button("Save Changes")

                if edit:
                    if new_name.strip():
                        tasks[index]["name"] = new_name.strip()
                        tasks[index]["deadline"] = new_deadline
                        tasks[index]["priority"] = new_priority
                        save_tasks()
                        st.success("Task updated!")
                        st.rerun()
                    else:
                        st.warning("Task name cannot be empty.")

            col1, col2 = st.columns(2)

            with col1:
                if not task["completed"]:
                    if st.button(
                        "Mark Completed",
                        key=f"complete_{index}"
                    ):
                        tasks[index]["completed"] = True
                        save_tasks()
                        st.rerun()

            with col2:
                if st.button("Delete Task", key=f"delete_{index}"):
                    tasks.pop(index)
                    save_tasks()
                    st.rerun()

# Downloads
elif page == "Downloads":
    st.header("📥 Download Your Tasks")

    if tasks:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "Task Name", "Deadline", "Priority", "Status"
        ])

        for task in tasks:
            status = "Completed" if task["completed"] else "Pending"
            writer.writerow([
                task["name"],
                task["deadline"],
                task["priority"],
                status
            ])

        st.download_button(
            "Download Tasks as CSV",
            data=output.getvalue(),
            file_name="my_tasks.csv",
            mime="text/csv"
        )
    else:
        st.info("No tasks available to download.")

st.divider()
st.caption("Smart Deadline Reminder | Built with Python and Streamlit")
