import streamlit as st

def init_session():
    if 'edit_mode' not in st.session_state:
        st.session_state.edit_mode = False

    if 'edit_index' not in st.session_state:
        st.session_state.edit_index = -1

    if 'edit_type' not in st.session_state:
        st.session_state.edit_type = 'Misc'

    if 'edit_text' not in st.session_state:
        st.session_state.edit_text = ''
