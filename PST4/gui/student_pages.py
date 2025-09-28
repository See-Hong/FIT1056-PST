import streamlit as st
from streamlit import session_state


def student_management_page(manager):
    """Renders all components for the student management page."""
    st.set_page_config(layout="wide", page_title="Student Management")
    st.header("Student Management")

    students = [(student.id, student.name) for student in manager.students]
    courses = [(course.id, course.name) for course in manager.courses]


    # --- Search Section ---
    search_function(manager)

    # --- Registration Section ---
    register_function(manager, courses)

    # --- Enrolling section ---
    enrollment_function(manager, students, courses)

    # --- Update section ---
    student_update_function(manager, students)

    # --- Attendance section ---


    # --- Remove section ---
    remove_student_function(manager, students)

def search_function(manager):
    st.subheader("Find a Student")
    with st.container(border=True):
        text = st.text_input("Student Name or ID").strip()
        df = manager.student_to_df()
        if text.isdigit():
            df = df[df["id"] == int(text)]
        elif text:
            df = df[df["name"].str.contains(text, case=False)]
        st.dataframe(df, hide_index=True)

def register_function(manager, courses):
    st.subheader("Register New Student")
    with st.form("registration_form"):
        reg_name = st.text_input("New Student Name").strip()
        reg_course = course_selectbox("Register Student", courses, key="register_course")
        submit = st.form_submit_button("Register Student", key="student_register")

        if submit:
            if reg_name and reg_course:
                course_id = reg_course[0]
                new_student = manager.register_student(reg_name, course_id)
                if new_student:
                    st.success(f"Successfully registered {reg_name}!")
                else:
                    st.error("Unable to register student, please try again.")
            else:
                st.warning("Please enter both a name and an instrument.")

def enrollment_function(manager, students, courses):
    st.subheader("Course Enrollment and Disenrollment")
    enrol_type = st.radio("Type", options=["Course Enrollment", "Course Disenrollment", "Switch Courses"])

    if enrol_type != "Switch Courses":
        with st.form("enrol_manager_form"):
            sel_student = student_selectbox("Student Name", students, "enrol_student")

            sel_course = course_selectbox("Course", courses, "enrol_course")

            submit = st.form_submit_button("Confirm", key="student_enrollment")
            if submit:
                if sel_student and sel_course:
                    student_id = sel_student[0]
                    course_id = sel_course[0]
                    if enrol_type == "Course Enrollment":
                        if manager.enrol_student(student_id, course_id):
                            st.success(f"Successfully enrolled student in {sel_course[1]}")
                        else:
                            st.error(f"Student already enrolled in {sel_course[1]}")
                    else:
                        if manager.disenroll_student(student_id, course_id):
                            st.success(f"Successfully disenrolled student in {sel_course[1]}")
                        else:
                            st.error(f"Student not enrolled in {sel_course[1]}")
                else:
                    st.warning("Please select a student and a course")
    else:
        with st.form("course_switch_form"):
            sel_student = student_selectbox("Student Name", students, key="switch_student")
            old_course = course_selectbox("Current Course", courses, key="switch_course")
            new_course = course_selectbox("Course To Switch To", courses, key="switch_course_2")
            submit = st.form_submit_button("Confirm")
            if submit:
                if sel_student and old_course and new_course:
                    switch = manager.switch_course(sel_student[0], from_course_id=old_course[0], to_course_id=new_course[0])
                    if switch:
                        st.success("Successfully switched student course")
                    else:
                        st.error("Unable to switch student course. Please check student enrolled courses.")
                else:
                    st.warning("Please select all options.")

def student_update_function(manager, students):
    st.subheader("Update student information")
    sel_student = student_selectbox("Student Name", students, key="update_student")
    if sel_student:
        with st.form("update_student_form"):
            new_name = st.text_input("New Student Name",value=sel_student[1]).strip()
            submit = st.form_submit_button("Save Changes", key="student_update")
            if submit:
                if new_name:
                    update = manager.update_information(sel_student[0], name=new_name)
                    if update:
                        st.success("Successfully changed student information")
                    else:
                        st.error("Unable to update student information. Please try again")
                else:
                    st.warning("Student name must not be blank")

def remove_student_function(manager, students):
    st.subheader("Remove a student")
    sel_student = student_selectbox("Student Name", students, key="remove_student")
    if sel_student:
        df = manager.student_to_df()
        st.dataframe(df[df["id"] == sel_student[0]], hide_index=True)
        with st.form("remove_student_form"):
            submit = st.form_submit_button("Confirm", key="student_remove")
            if submit:
                manager.remove_student(sel_student[0])
                st.success("Successfully removed student")
            else:
                st.error("Unable to remove student. Please try again")

def student_selectbox(label, students, key):
    s_placeholder = "Select a student"

    if students:
        options = [s_placeholder] + students
        disabled = False
    else:
        options = ["No students available"]
        disabled = True

    choice = st.selectbox(label, options=options, disabled=disabled, key=key, format_func=format_option)

    if disabled or choice == s_placeholder:
        return None
    else:
        return choice

def course_selectbox(label, courses, key):

    s_placeholder = "Select a course"

    if courses:
        options = [s_placeholder] + courses
        disabled = False
    else:
        options = ["No students available"]
        disabled = True

    choice = st.selectbox(label, options=options, disabled=disabled, key=key, format_func=format_option)

    if disabled or choice == s_placeholder:
        return None
    else:
        return choice

def format_option(c):
    if type(c) == tuple:
        return c[1]
    else:
        return c