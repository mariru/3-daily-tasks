import streamlit as st
from datetime import date
from modules.task_manager import Task
from functools import partial

def add_task(task_type):
    def call_back():
        new_task = Task(st.session_state[f'{task_type}_task_input'], task_type)
        st.session_state.Open_Tasks.add(new_task)
        st.session_state[f'{task_type}_task_input'] = ''
    return call_back

def save_edit():
    ## TODO
    st.session_state.Open_Tasks.edit(st.session_state.edit_type, st.session_state.edit_index, st.session_state.edit_text)
    st.session_state.edit_mode = False
    st.session_state.edit_index = -1
    st.session_state.edit_type = 'Misc'
    st.session_state.edit_text = ''

def edit_mode_ui(tab='Daily'):
    with st.form("edit_form"):
        new_task_name = st.text_input("Edit task:", value=st.session_state.edit_text)
        col0, col1, col2 = st.columns([0.7, 0.15, 0.15])
        with col1:
            if st.form_submit_button("Save"):
                #TODO Daily -> Monthly/Weekly as necessary
                st.session_state[f'{tab}_Tasks'].edit(st.session_state.edit_type, st.session_state.edit_index, new_task_name)
                st.session_state.edit_mode = False
                st.rerun()
        with col2:
            if st.form_submit_button("Cancel"):
                st.session_state.edit_mode = False
                st.rerun()
    st.stop()  # Prevents the rest of the app from running while in edit mode
    # Edit mode
    #if st.session_state.edit_mode:
    #   st.text_input("Edit task:", key=f'{task_type}_edit_text', on_change=save_edit)


def input_task_ui(Task_List):
    st.markdown('### Add new task')
    task_container = st.container()
    with task_container:
                col1, col2 = st.columns([0.4, 0.6])
                with col1:
                    task_type = st.selectbox('Select a Task Type', Task_List.task_types)
                with col2:
                    st.text_input("Enter a task:", key='new_task_input', on_change=partial(Task_List.add_task_callback, task_type ))
                    

def task_list_display_ui(Task_List, tab='Daily'):
    for task_type in Task_List.task_types:
        if len(Task_List.tasks[task_type]) > 0:
            st.markdown(f'### {tab} {task_type} Tasks')
            Task_List.print(task_type)

    

def progress_display_ui(Task_List, tab = 'Daily'):
        
    st.title(f'{tab} Tasks for {date.today().strftime("%B %-d, %Y:")}')


    progress, completed_tasks, total_tasks = Task_List.progress()
    st.header(f"Progress: {completed_tasks}/{total_tasks} tasks completed")
    st.progress(progress)

    # Show congratulatory message if all tasks are done
    if completed_tasks == total_tasks and total_tasks > 0:
        st.balloons()
        time_window = {'Daily': 'today', 'Weekly': 'this week', 'Monthly': 'this month'}
        st.success(f"Congrats! You finished all your tasks for {time_window[tab]}. Enjoy the rest of your day and don't forget to floss!")
