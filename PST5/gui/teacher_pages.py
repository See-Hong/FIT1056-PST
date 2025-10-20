import streamlit as st
from utils.utils import *


def teacher_management_page(manager):
    """Renders all components for the student management page."""
    st.set_page_config(layout="wide", page_title="Teacher Management")
    st.header("Teacher Management")

    # Data List
    teachers = [(teacher.id, teacher.name) for teacher in manager.teachers]
    specialty = [teacher.specialty for teacher in manager.teachers]
    # Returns a list with no duplicates
    specialty = list(set(specialty))


    search_function(manager)

    if st.session_state.logged_in:
        add_teacher_function(manager, specialty)

        teacher_update_function(manager, teachers, specialty)

        remove_teacher_function(manager, teachers)

def search_function(manager):
    """Renders the teacher search function"""
    st.subheader("Find a Teacher")
    with st.container(border=True):
        text = st.text_input("Teacher Name or ID").strip()
        df = manager.teacher_to_df()

        # Checks if term is name or id
        if text.isdigit():
            df = df[df["id"] == int(text)]
        elif text:
            df = df[df["name"].str.contains(text, case=False)]
        st.dataframe(df, hide_index=True)

def add_teacher_function(manager, specialty):
    """Renders the add teacher function"""
    st.subheader("Add New Teacher")
    with st.form("add_teacher_form"):

        # Add teacher form
        reg_name = st.text_input("New Teacher Name").strip()
        reg_specialty = specialty_selectbox("Teacher Specialty", specialty, key="add_teacher_specialty", accept_new_options=True)
        submit = st.form_submit_button("Add Teacher", key="add_teacher_submit")

        if submit:
            if reg_name and reg_specialty:
                new_teacher = manager.add_teacher(reg_name, reg_specialty)
                if new_teacher:
                    st.success(f"Successfully added teacher {reg_name}")
                else:
                    st.error("Unable to add teacher. Please try again.")
            else:
                st.warning("Please enter both a name and a specialty.")

def teacher_update_function(manager, teachers, specialty):
    """Renders the teacher updating form"""
    st.subheader("Update teacher information")
    with st.container(border=True):

        # Teacher selection box
        sel_teacher = teacher_selectbox("Teacher Name", teachers, key="update_teacher")
        if sel_teacher:
            with st.form("update_teacher_form"):
                # Renders the teacher update form with current information as default values
                new_name = st.text_input("New Teacher Name",value=sel_teacher[1]).strip()
                new_specialty = specialty_selectbox("New Specialty", specialty, key="update_teacher_specialty")
                submit = st.form_submit_button("Save Changes", key="teacher_update")

                if submit:
                    # Gets the updated data
                    update_dict = {}
                    if new_name:
                        update_dict["name"] = new_name
                        if new_specialty:
                            update_dict["specialty"] = new_specialty
                        update = manager.update_information(sel_teacher[0], **update_dict, type_="teacher")
                        if update:
                            st.success("Successfully changed teacher information")
                        else:
                            st.error("Unable to update teacher information. Please try again")
                    else:
                        st.warning("Teacher name must not be blank")

def remove_teacher_function(manager, teachers):
    """Renders the remove teacher function"""
    st.subheader("Remove a teacher")
    with st.container(border=True):

        # Teacher selection box
        sel_teacher = teacher_selectbox("Teacher Name", teachers, key="remove_teacher")
        if sel_teacher:

            # Shows the teacher information
            df = manager.teacher_to_df()
            st.dataframe(df[df["id"] == sel_teacher[0]], hide_index=True)
            with st.form("remove_teacher_form"):
                submit = st.form_submit_button("Confirm", key="teacher_remove")
                if submit:
                    remove = manager.remove_teacher(sel_teacher[0])
                    if remove:
                        st.success("Successfully removed teacher")
                    else:
                        st.error("Unable to remove teacher. Please try again")

