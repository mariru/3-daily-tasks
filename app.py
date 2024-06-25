import streamlit as st
from modules.daily_tasks import daily_tasks_ui
from modules.weekly_tasks import weekly_tasks_ui
from modules.monthly_tasks import monthly_tasks_ui
from utils.session_utils import init_session

init_session()
# Sidebar with tabs
with st.sidebar:
    st.markdown('### Task Horizon')
    tabs = st.radio(" ", ["Daily Tasks", "Weekly Tasks", "Monthly Tasks"])

if tabs == "Daily Tasks":
    daily_tasks_ui()

elif tabs == "Weekly Tasks":
    st.header("Coming Soon")
    weekly_tasks_ui()

elif tabs == "Monthly Tasks":
    st.header("Coming Soon")
    monthly_tasks_ui()