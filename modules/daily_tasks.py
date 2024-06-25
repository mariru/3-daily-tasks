import streamlit as st
from utils.ui_utils import *
from modules.task_manager import Task, Task_List
from datetime import date


Daily_Task_Types = ['Basic', 'Prototyping', 'Learning']

def daily_tasks_ui():
    if 'Daily_Tasks' not in st.session_state:
        st.session_state.Daily_Tasks = Task_List(task_types = Daily_Task_Types)
        # create basic tasks:
        new_task = Task('Morning Pages', 'Basic')
        st.session_state.Daily_Tasks.add(new_task)
        new_task = Task('TypingClub', 'Basic')
        st.session_state.Daily_Tasks.add(new_task)
        new_task = Task('Document Progress and Insights', 'Basic')
        st.session_state.Daily_Tasks.add(new_task)

    if st.session_state.edit_mode:
        edit_mode_ui('Daily')

    progress_display_ui(st.session_state.Daily_Tasks, 'Daily')

    task_list_display_ui(st.session_state.Daily_Tasks, 'Daily')

    input_task_ui(st.session_state.Daily_Tasks)

    # Archive button to remove completed tasks
    #if st.button("Archive Completed Tasks"):
    #    st.session_state.Daily_Tasks.archive()
    #    st.rerun()  # To refresh the app and update the task list