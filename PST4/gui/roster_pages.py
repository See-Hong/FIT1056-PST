# gui/roster_pages.py
import streamlit as st
import pandas as pd
import datetime as dt


def show_roster_page(manager):
    """Renders the daily roster and check-in functionality."""
    st.set_page_config(layout="wide", page_title="Roster management")
    st.header("Daily Roster")

    students = [(student.id, student.name) for student in manager.students]
    courses = [(course.id, course.name) for course in manager.courses]

    # --- View Roster Section ---
    current_day_roster(manager)

    # --- Student Check-in Section ---
    student_check_in(manager, students, courses)

    # --- Student Attendance ---
    student_attendance(manager, students, courses)

def current_day_roster(manager):
    with st.container(border=True):
        day = st.selectbox("Select a day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])

        if day:
            lessons = manager.daily_roster(day)
            if lessons:
                df = pd.DataFrame(lessons)
                st.dataframe(df)
            else:
                st.error("No lessons available for the day")

def student_check_in(manager, students, courses):
    st.subheader("Student Check-in")
    with st.form("check_in_form"):

        sel_student = student_selectbox("Student Name", students, key="check_in_student")
        sel_course = course_selectbox("Course Name", courses, key="check_in_courses")
        sel_date = st.date_input("Check In Date", value="today", max_value="today", min_value=dt.date(2025, 1, 1))
        sel_time = st.time_input("Check In Time", value="now", step=600)

        submit = st.form_submit_button("Check-in Student", key="check_in_submit")

        if submit:
            st.text(sel_student)
            if sel_student and sel_course:
                student_id = sel_student[0]
                course_id = sel_course[0]
                timestamp = dt.datetime.combine(sel_date, sel_time)

                check_in = manager.check_in(student_id, course_id, timestamp)

                if check_in:
                    st.success(f"Checked in {sel_student[1]} for {sel_course[1]}")
                else:
                    st.error("Check-in failed. Student may not be enrolled in course.")
            else:
                st.warning("Please select a student and course")

def student_attendance(manager, students, courses):
    st.subheader("Check student attendance")
    with st.container(border=True):
        sel_student = student_selectbox("Student Name", students, key="student_attendance")
        sel_course = course_selectbox("Course Name", courses, key="attendance_course")
        attendance_log = manager.attendance_log
        formatted_log = []
        for record in attendance_log:
            course = manager.find_by_id(record["course_id"], search="course")
            formatted_log.append(
                {
                    "student_id": record["student_id"],
                    "course_id": record["course_id"],
                    "course": course.name,
                    "timestamp": pd.to_datetime(record["timestamp"].replace("T", " ")),
                }
            )
        df = pd.DataFrame(formatted_log)
        if sel_student and not sel_course:
            df = df[df["student_id"] == sel_student[0]]
        elif sel_course and not sel_student:
            df = df[df["course_id"] == sel_course[0]]
        elif sel_student and sel_course:
            df = df[(df["student_id"] == sel_student[0]) & (df["course_id"] == sel_course[0])]
        if df.empty:
            st.error("No matching attendance records found")
        else:
            st.dataframe(df, hide_index=True)

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
        return f"{c[0]} {c[1]}"
    else:
        return c