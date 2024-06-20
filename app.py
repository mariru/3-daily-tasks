import streamlit as st
from datetime import date

class Task:
    def __init__(self, name):
        self.name = name
        self.done = False
        self.date = date.today()

class Task_List:
    def __init__(self, max_tasks=-1):
        self.max_tasks = max_tasks
        self.tasks = []

    def add(self, task):
        if len(self.tasks) == self.max_tasks:
            st.warning("Maximum number of tasks reached.")
        else:
            self.tasks.append(task)
    def print(self):
        for task in self.tasks:
            if st.checkbox(f"{task.date.strftime('%B %-d, %Y:')} {task.name}", value=task.done):
                if not task.done:
                    task.done = True
                    st.rerun()
            else:
                if task.done:
                    task.done = False
                    st.rerun()


    def archive(self):
        self.tasks = [task for task in self.tasks if not task.done]

if 'Open_Tasks' not in st.session_state:
    st.session_state.Open_Tasks = Task_List(3) 

def add_task():
    new_task = Task(st.session_state.task_input)
    st.session_state.Open_Tasks.add(new_task)
    st.session_state.task_input = ''

# Title of the app
st.title('3 Daily Tasks')

total_tasks = len(st.session_state['Open_Tasks'].tasks)
completed_tasks = sum(task.done for task in st.session_state['Open_Tasks'].tasks)
progress = completed_tasks / total_tasks if total_tasks > 0 else 0
st.write(f"Progress: {completed_tasks}/{total_tasks} tasks completed")
st.progress(progress)

if completed_tasks == total_tasks and total_tasks > 0:
    st.balloons()
    st.success("Congrats! You finished all your tasks for today. Enjoy the rest of your day and don't forget to floss!")

# Prompt for user input
st.text_input("Enter a task:", key = 'task_input', on_change=add_task)


# Display tasks
st.session_state.Open_Tasks.print()

# Archive button to remove completed tasks
if st.button("Archive Completed Tasks"):
    st.session_state.Open_Tasks.archive()
    st.rerun()

