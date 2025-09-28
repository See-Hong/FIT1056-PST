import streamlit as st
# from app4.schedule import ScheduleManager
import app4.schedule as schedule
from gui.student_pages import student_management_page
from gui.overview import overview_page
from gui.roster_pages import show_roster_page
import importlib


def launch():
    """Sets up the main Streamlit application window and navigation."""
    st.set_page_config(layout="wide", page_title="Music School Management System")

    if 'manager' not in st.session_state:
        st.session_state.manager = schedule.ScheduleManager()

    importlib.reload(schedule)
    st.session_state.manager = schedule.ScheduleManager()

    st.sidebar.title("MSMS Navigation")

    # Create a radio button menu in the sidebar for page navigation.
    page = st.sidebar.radio("Go to", ["Home", "Student Management", "Daily Roster", "Course Management", "Teacher Management", "Payments (stub)"])

    # Use an if/elif block to call the correct function to render the selected page.
    if page == "Home":
        overview_page(st.session_state.manager)
    elif page == "Student Management":
        student_management_page(st.session_state.manager)
    elif page == "Daily Roster":
        show_roster_page(st.session_state.manager)
    elif page == "Course Management":
        pass
    elif page == "Teacher Management":
        pass
    elif page == "Payments (stub)":
        st.header("Payments")
        st.warning("This feature will be implemented in PST5.")



