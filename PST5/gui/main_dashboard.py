import streamlit as st
from app.schedule import ScheduleManager
from gui.student_pages import student_management_page
from gui.overview import overview_page
from gui.roster_pages import show_roster_page
from gui.course_pages import course_management_page
from gui.teacher_pages import teacher_management_page
from gui.finance_pages import show_finance_page
from utils.utils import *


def launch():
    """Sets up the main Streamlit application window and navigation."""
    st.set_page_config(layout="wide", page_title="Music School Management System")

    if 'manager' not in st.session_state:
        st.session_state.manager = ScheduleManager()

    if 'first_run' not in st.session_state:
        st.session_state.first_run = True
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.active_page = "Home"

    pages = [("Home", overview_page),
             ("Student Management", student_management_page),
             ("Daily Roster", show_roster_page),
             ("Course Management", course_management_page),
             ("Teacher Management", teacher_management_page),
             ("Payments", show_finance_page)]

    def switch_page(name):
        """Function for highlighting current page"""
        st.session_state.active_page = name
    # Sidebar navigation
    st.sidebar.title("Music School Management System")
    st.sidebar.divider()
    for page in pages:
        button_type = "primary" if page[0] == st.session_state.active_page else "secondary"
        st.sidebar.button(page[0], type=button_type, width="stretch", on_click=switch_page, args=[page[0]], key=f"page-{page[0]}")
    st.sidebar.divider()

    for page in pages:
        if st.session_state.active_page == page[0]:
            page[1](st.session_state.manager)

    # Login
    if not st.session_state.logged_in:
        st.sidebar.button("Sign in/Sign up", on_click=signing_in, key="signing_in")
    else:
        with st.sidebar.container():
            if st.session_state.user:
                st.write(f"Hello {st.session_state.user["username"]}!")
                st.button("Log Out", type="primary", width="stretch", on_click=log_out)

