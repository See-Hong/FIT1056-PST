import streamlit as st
from app4.schedule import ScheduleManager
from gui.student_pages import student_management_page
from gui.overview import overview_page


def launch():
    """Sets up the main Streamlit application window and navigation."""
    st.set_page_config(layout="wide", page_title="Music School Management System")

    # Instantiate the "brain" of our app ONCE and store it in the session state.
    # This is crucial so the manager object persists as we switch pages.
    if 'manager' not in st.session_state:
        st.session_state.manager = ScheduleManager()

    st.sidebar.title("MSMS Navigation")

    # Create a radio button menu in the sidebar for page navigation.
    page = st.sidebar.radio("Go to", ["Home", "Student Management", "Daily Roster", "Payments (stub)"])

    # Use an if/elif block to call the correct function to render the selected page.
    if page == "Home":
        overview_page(st.session_state.manager)
    elif page == "Student Management":
        student_management_page(st.session_state.manager)
    # elif page == "Daily Roster":
    #     show_roster_page(st.session_state.manager)
    # elif page == "Payments (stub)":
    #     st.header("Payments")
    #     st.warning("This feature will be implemented in PST5.")



