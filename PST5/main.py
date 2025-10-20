from gui.main_dashboard import launch
from app.admin_utils import init_logger, backup_data
import streamlit as st

if __name__ == "__main__":
    if "start" not in st.session_state:
        init_logger()
        backup_data()
        st.session_state.start = True
    launch()