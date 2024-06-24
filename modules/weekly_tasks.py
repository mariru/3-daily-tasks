import streamlit as st
from utils.ui_utils import display_tasks
from modules.task_manager import TaskManager

task_manager = TaskManager("data/weekly_tasks.json")

def weekly_tasks_ui():
    # TODO; first finish daily tasks ui then adapt (inherit) from there!
    weekly_tasks = task_manager.tasks

    # Display tasks
    display_tasks(weekly_tasks, task_manager.toggle_task)

    # Add new task
    new_task = st.text_input("Enter new weekly task")
    if st.button("Add Weekly Task"):
        task_manager.add_task(new_task)
        st.experimental_rerun()