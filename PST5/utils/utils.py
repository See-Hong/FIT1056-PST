import streamlit as st

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

def specialty_selectbox(label, specialty, key, **kwargs):
    s_placeholder = "Select a specialty"

    if specialty:
        options = [s_placeholder] + specialty
        disabled = False
    else:
        options = ["No specialties available"]
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