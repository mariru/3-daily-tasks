import streamlit as st
from modules.daily_tasks import daily_tasks_ui
from modules.weekly_tasks import weekly_tasks_ui
from modules.monthly_tasks import monthly_tasks_ui
from utils.session_utils import init_session

init_session()
# Sidebar with tabs
tabs = st.sidebar.radio("Tasks", ["Daily Tasks", "Weekly Tasks", "Monthly Tasks"])
print(tabs)
if tabs == "Daily Tasks":
    st.header("Daily Tasks")
    print("Hello world")
    daily_tasks_ui()
    print("stop")

elif tabs == "Weekly Tasks":
    st.header("Weekly Tasks")
    weekly_tasks_ui()

elif tabs == "Monthly Tasks":
    st.header("Monthly Tasks")
    monthly_tasks_ui()