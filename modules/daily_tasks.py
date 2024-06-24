import streamlit as st
from utils.ui_utils import display_tasks
from modules.task_manager import Task, Task_List
from datetime import date


Task_Types = ['Basic', 'Prototyping', 'Learning']

def daily_tasks_ui():
    if 'Daily_Tasks' not in st.session_state:
        st.session_state.Daily_Tasks = Task_List(3, Task_Types)
    # create basic tasks:
    new_task = Task('Morning Pages', 'Basic')
    st.session_state.Daily_Tasks.add(new_task)
    new_task = Task('TypingClub', 'Basic')
    st.session_state.Daily_Tasks.add(new_task)

    if st.session_state.edit_mode:
        edit_mode_ui('Daily')
        
    st.title(f'Daily Tasks for {date.today().strftime("%B %-d, %Y:")}')

    # TODO: each task list should have its own progress (part of the TaskList class)
    # progress is updated each time a task is added, deleted, marked as complete, unchecked...
    total_tasks = sum(len(st.session_state.Daily_Tasks.tasks[t]) for t in Task_Types)
    completed_tasks = sum(task.done for t in Task_Types for task in st.session_state.Daily_Tasks.tasks[t])

    progress = completed_tasks / total_tasks if total_tasks > 0 else 0
    st.header(f"Progress: {completed_tasks}/{total_tasks} tasks completed")
    st.progress(progress)

    # Show congratulatory message if all tasks are done
    if completed_tasks == total_tasks and total_tasks > 0:
        st.balloons()
        st.success("Congrats! You finished all your tasks for today. Enjoy the rest of your day and don't forget to floss!")

    for task_type in Task_Types:
        st.subheader(f'Daily {task_type} Tasks')
        #if not task_type == 'Basic':
        #    st.text_input(f"Enter a {task_type.lower()} task:", key=f'{task_type}_task_input', on_change=add_task(task_type))

        # Display tasks
        st.session_state.Daily_Tasks.print(task_type)

        # Edit mode
        if st.session_state.edit_mode:
            st.text_input("Edit task:", key=f'{task_type}_edit_text', on_change=save_edit)

    # Archive button to remove completed tasks
    if st.button("Archive Completed Tasks"):
        st.session_state.Daily_Tasks.archive()
        st.rerun()  # To refresh the app and update the task list