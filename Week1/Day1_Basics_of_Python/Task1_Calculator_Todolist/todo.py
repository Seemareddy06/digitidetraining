import streamlit as st

# Initialize session state for tasks
if "tasks" not in st.session_state:
    st.session_state.tasks = []

st.title("📝 My To-Do List")

# Input box to add new task
new_task = st.text_input("Add a new task...")

# Add task button
if st.button("➕ Add Task"):
    if new_task.strip():
        st.session_state.tasks.append(new_task)
        st.success(f"Task added: {new_task}")
    else:
        st.warning("Please enter a valid task!")

st.subheader("Your Tasks")

if st.session_state.tasks:
    for i, task in enumerate(st.session_state.tasks):
        col1, col2 = st.columns([8, 1])
        col1.write(f"{i+1}. {task}")
        if col2.button("❌", key=f"del{i}"):
            st.session_state.tasks.pop(i)
            st.experimental_rerun()
else:
    st.info("No tasks in the list.")
