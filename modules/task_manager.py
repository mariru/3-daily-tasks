import streamlit as st
from datetime import date


class TaskManager:
    def __init__(self, task_file):
        self.task_file = task_file
        self.tasks = self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.task_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_tasks(self):
        with open(self.task_file, "w") as file:
            json.dump(self.tasks, file)

    def add_task(self, task):
        self.tasks.append({"text": task, "completed": False})
        self.save_tasks()

    def toggle_task(self, index):
        self.tasks[index]['completed'] = not self.tasks[index]['completed']
        self.save_tasks()

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
