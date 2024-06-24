import streamlit as st

def display_tasks(tasks, toggle_task):
    for index, task in enumerate(tasks):
        task_text = task['text']
        if task['completed']:
            task_text = f"~~{task_text}~~"  # Strikethrough completed tasks
        if st.checkbox(task_text, value=task['completed'], key=f"task_{index}"):
            toggle_task(index)
            st.rerun()

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
