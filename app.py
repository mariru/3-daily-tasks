import streamlit as st
from datetime import date
from functools import partial
from streamlit_extras.let_it_rain import rain
import time

def single_task_success():
    rain(
        emoji="🎈",
        font_size=54,
        falling_speed=3,
        animation_length=10,
    )
    time.sleep(2)

class Task:
    def __init__(self, name, task_type='Misc'):
        self.name = name
        self.done = False
        self.date = date.today()
        self.task_type = task_type

class Task_List:
    def __init__(self, max_tasks=-1, task_types = ['Misc']):
        self.max_tasks = max_tasks
        self.task_types = task_types
        self.tasks = {}
        for t in task_types:
            self.tasks[t] = []

    def add(self, task):
        if task.task_type not in self.tasks:
            raise NotImplementedError
        if len(self.tasks[task.task_type]) == self.max_tasks:
            st.warning("Maximum number of tasks reached.")
        else:
            self.tasks[task.task_type].append(task)

    def delete(self, task_type, index):
        if 0 <= index < len(self.tasks[task_type]):
            del self.tasks[task_type][index]

    def edit(self, task_type, index, new_name):
        if 0 <= index < len(self.tasks[task_type]):
            self.tasks[task_type][index].name = new_name

    def print(self, task_type):
        for i, task in enumerate(self.tasks[task_type]):
            task_container = st.container()
            with task_container:
                col1, col2, col3 = st.columns([0.8, 0.1, 0.1])
                with col1:
                    if st.checkbox(task.name, value=task.done, key=f"{task_type}_{i}"):
                        if not task.done:
                            task.done = True
                            single_task_success()
                            st.rerun()
                    else:
                        if task.done:
                            task.done = False
                            st.rerun()
                with col2:
                    if st.button("✏️", key=f"edit_button_{task_type}_{i}"):
                        st.session_state.edit_index = i
                        st.session_state.edit_type = task_type
                        st.session_state.edit_mode = True
                        st.session_state.edit_text = task.name
                        st.rerun()
                with col3:
                    if st.button("🗑️", key=f"delete_button_{task_type}_{i}"):
                        self.delete(task_type, i)
                        st.rerun()

    def archive(self):
        for t in self.task_types:
            self.tasks[t] = [task for task in self.tasks[t] if not task.done]

Task_Types = ['Basic', 'Prototyping', 'Learning']
# Initialize Task_List in session state if not already present
if 'Open_Tasks' not in st.session_state:
    st.session_state.Open_Tasks = Task_List(3, Task_Types)
    # create basic tasks:
    new_task = Task('Morning Pages', 'Basic')
    st.session_state.Open_Tasks.add(new_task)
    new_task = Task('TypingClub', 'Basic')
    st.session_state.Open_Tasks.add(new_task)
    
if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False

if 'edit_index' not in st.session_state:
    st.session_state.edit_index = -1

if 'edit_type' not in st.session_state:
    st.session_state.edit_type = 'Misc'

if 'edit_text' not in st.session_state:
    st.session_state.edit_text = ''

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

if st.session_state.edit_mode:
    with st.form("edit_form"):
        new_task_name = st.text_input("Edit task:", value=st.session_state.edit_text)
        col0, col1, col2 = st.columns([0.7, 0.15, 0.15])
        with col1:
            if st.form_submit_button("Save"):
                st.session_state.Open_Tasks.edit(st.session_state.edit_type, st.session_state.edit_index, new_task_name)
                st.session_state.edit_mode = False
                st.rerun()
        with col2:
            if st.form_submit_button("Cancel"):
                st.session_state.edit_mode = False
                st.rerun()
    st.stop()  # Prevents the rest of the app from running while in edit mode


# Progress tracking
st.title(f'Daily Tasks for {date.today().strftime("%B %-d, %Y:")}')
total_tasks = sum(len(st.session_state.Open_Tasks.tasks[t]) for t in Task_Types)
completed_tasks = sum(task.done for t in Task_Types for task in st.session_state.Open_Tasks.tasks[t])

progress = completed_tasks / total_tasks if total_tasks > 0 else 0
st.header(f"Progress: {completed_tasks}/{total_tasks} tasks completed")
st.progress(progress)

# Show congratulatory message if all tasks are done
if completed_tasks == total_tasks and total_tasks > 0:
    st.balloons()
    st.success("Congrats! You finished all your tasks for today. Enjoy the rest of your day and don't forget to floss!")

for task_type in Task_Types:
    st.subheader(f'Daily {task_type} Tasks')
    if not task_type == 'Basic':
        st.text_input(f"Enter a {task_type.lower()} task:", key=f'{task_type}_task_input', on_change=add_task(task_type))

    # Display tasks
    st.session_state.Open_Tasks.print(task_type)

    # Edit mode
    if st.session_state.edit_mode:
        st.text_input("Edit task:", key=f'{task_type}_edit_text', on_change=save_edit)

# Archive button to remove completed tasks
if st.button("Archive Completed Tasks"):
    st.session_state.Open_Tasks.archive()
    st.rerun()  # To refresh the app and update the task list