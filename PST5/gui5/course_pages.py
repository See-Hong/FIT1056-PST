import pandas as pd
import streamlit as st


def course_management_page(manager):
    """Renders all components for the course management page."""
    st.set_page_config(layout="wide", page_title="Course Management")
    st.header("Course Management")

    courses = [(course.id, course.name) for course in manager.courses]
    teachers = [(teacher.id, teacher.name) for teacher in manager.teachers]
    instruments = [course.instrument for course in manager.courses]
    instruments = list(set(instruments))


    search_function(manager)

    add_course_function(manager, teachers, instruments)

    course_update_function(manager, courses, instruments, teachers)

    remove_course_function(manager, courses)

    lessons_search_function(manager, courses)

    add_lesson_function(manager, courses)

def search_function(manager):
    """Renders the course search function"""
    st.subheader("Find a Course")
    with st.container(border=True):
        text = st.text_input("Course Name or ID").strip()
        df = manager.course_to_df()

        # Checks if the term is name or ID
        if text.isdigit():
            df = df[df["id"] == int(text)]
        elif text:
            df = df[df["name"].str.contains(text, case=False)]
        st.dataframe(df, hide_index=True)

def add_course_function(manager, teachers, instruments):
    """Renders the add course function"""
    st.subheader("Add new course")
    with st.form("add_course_form"):

        # Add course form
        reg_name = st.text_input("New Course Name").strip()
        reg_instrument = instrument_selectbox("Course Instrument", instruments, key="add_course_instrument", accept_new_options=True)
        reg_teacher = teacher_selectbox("Course Teacher", teachers, key="add_course_teacher")
        submit = st.form_submit_button("Add Course", key="add_course")

        if submit:
            if reg_name and reg_instrument and reg_teacher:
                new_course = manager.add_course(reg_name, reg_instrument, reg_teacher[0])
                if new_course:
                    st.success(f"Successfully added course {reg_name}")
                else:
                    st.error("Unable to add course. Please try again")
            else:
                st.warning("Please fill in all selections")

def course_update_function(manager, courses, instruments, teachers):
    """Renders the course updating function"""
    st.subheader("Update course information")
    with st.container(border=True):

        # Course selection box
        sel_course = course_selectbox("Course Name", courses, key="update_course")
        if sel_course:
            with st.form("update_course_form"):

                # Renders the course update form with current information as default values
                new_name = st.text_input("New Course Name",value=sel_course[1]).strip()
                new_instrument = instrument_selectbox("New Instrument", instruments, key="update_course_instrument", accept_new_options=True)
                new_teacher = teacher_selectbox("New Teacher", teachers, key="update_course_teacher")
                submit = st.form_submit_button("Save Changes", key="course_update")
                if submit:

                    # Gets the updated data
                    update_dict = {}
                    if new_name:
                        update_dict["name"] = new_name
                        if new_instrument:
                            update_dict["instrument"] = new_instrument
                        if new_teacher:
                            update_dict["teacher_id"] = new_teacher[0]
                        update = manager.update_information(sel_course[0], type_="course", **update_dict)
                        if update:
                            st.success("Successfully changed course information")
                        else:
                            st.error("Unable to update course information. Please try again")
                    else:
                        st.warning("Course name must not be blank")

def remove_course_function(manager, courses):
    """Renders the remove course function"""
    st.subheader("Remove a course")
    with st.container(border=True):

        # Course selection box
        sel_course = course_selectbox("Course Name", courses, key="remove_course")
        if sel_course:

            # Shows the course information
            df = manager.course_to_df()
            st.dataframe(df[df["id"] == sel_course[0]], hide_index=True)
            with st.form("remove_course_form"):
                submit = st.form_submit_button("Confirm", key="course_remove")
                if submit:
                    remove = manager.remove_course(sel_course[0])
                    if remove:
                        st.success("Successfully removed course")
                    else:
                        st.error("Unable to remove course. Please try again")

def lessons_search_function(manager, courses):
    """Renders the lesson search function"""
    st.subheader("Find a lesson")
    with st.container(border=True):

        # Search for lessons of a course
        sel_course = course_selectbox("Course Name", courses, key="lesson_course")
        if sel_course:
            course = manager.find_by_id(sel_course[0], search="course")
            lessons = [lesson for lesson in course.lessons]
            df = pd.DataFrame(lessons)
            if df.empty:
                st.error("No lessons found for this course")
            else:
                st.dataframe(df)

def add_lesson_function(manager, courses):
    """Renders the add lesson function"""
    st.subheader("Add a lesson")
    with st.form("add_lesson_form"):

        # Add lesson form
        sel_course = course_selectbox("Course Name", courses, key="add_lesson_course")
        lesson_day = st.selectbox("Lesson Day", options=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], key="add_lesson_day")
        start_time = st.time_input("Lesson Start Time", step=1800)
        room = st.text_input("Lesson Location", key="add_lesson_room").strip()
        submit = st.form_submit_button("Submit", key="add_lesson_submit")

        if submit:
            if sel_course:
                if lesson_day and start_time and room:
                    add = manager.add_lesson(sel_course[0], lesson_day, start_time, room)
                    if add:
                        st.success("Successfully added lesson to course")
                    else:
                        st.error("Unable to add lesson to course. Please try again")
                else:
                    st.warning("Please enter lesson details")
            else:
                st.warning("Please select a course")


def student_selectbox(label, students, key, **kwargs):
    s_placeholder = "Select a student"

    if students:
        options = [s_placeholder] + students
        disabled = False
    else:
        options = ["No students available"]
        disabled = True

    choice = st.selectbox(label, options=options, disabled=disabled, key=key, format_func=format_option, **kwargs)

    if disabled or choice == s_placeholder:
        return None
    else:
        return choice

def course_selectbox(label, courses, key, **kwargs):

    s_placeholder = "Select a course"

    if courses:
        options = [s_placeholder] + courses
        disabled = False
    else:
        options = ["No students available"]
        disabled = True

    choice = st.selectbox(label, options=options, disabled=disabled, key=key, format_func=format_option, **kwargs)

    if disabled or choice == s_placeholder:
        return None
    else:
        return choice

def teacher_selectbox(label, teachers, key, **kwargs):
    s_placeholder = "Select a teacher"

    if teachers:
        options = [s_placeholder] + teachers
        disabled = False
    else:
        options = ["No teachers available"]
        disabled = True
    choice = st.selectbox(label, options=options, disabled=disabled, key=key, format_func=format_option, **kwargs)

    if disabled or choice == s_placeholder:
        return None
    else:
        return choice

def instrument_selectbox(label, instruments, key, **kwargs):
    s_placeholder = "Select or add an instrument"

    if instruments:
        options = [s_placeholder] + instruments
        disabled = False
    else:
        options = ["No instruments available"]
        disabled = True

    choice = st.selectbox(label, options=options, disabled=disabled, key=key, format_func=format_option, **kwargs)

    if disabled or choice == s_placeholder:
        return None
    else:
        return choice

def format_option(c):
    if type(c) == tuple:
        return f"{c[0]} {c[1]}"
    else:
        return c