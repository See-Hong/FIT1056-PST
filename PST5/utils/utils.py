import streamlit as st
import re
import json
from werkzeug.security import generate_password_hash, check_password_hash

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

@st.dialog("Accounts")
def signing_in():
    account_data_file = "PST5/data/accounts.json"
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    option = st.radio("Options", options=["Sign In", "Sign Up"])
    with st.form("account_form"):
        if option == "Sign Up":
            name = st.text_input("Username", max_chars=20).strip()
        email = st.text_input("Email", max_chars=50).strip()
        password = st.text_input("Password", max_chars=20)
        submit = st.form_submit_button("Enter")
        if submit:
            if any(i.isspace() for i in password):
                st.warning("No whitespaces allowed in password.")
                return
            if not re.match(email_pattern, email):
                st.warning("Email invalid.")
                return
            if option == "Sign Up" and name.isspace():
                st.warning("Username must not be empty.")
                return

            try:
                with open(account_data_file, "r") as file:
                    data = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                data = {"users": []}
            if option == "Sign Up":
                if data["users"]:
                    for acc in data["users"]:
                        if acc["email"] == email:
                            st.error("Email already taken.")
                            return
                new_acc = {
                        "username": name,
                        "email": email,
                        "password": generate_password_hash(password, salt_length=16)
                }
                data["users"].append(new_acc)
                with open(account_data_file, mode="w") as file:
                    json.dump(data, fp=file, indent=3)
                st.success("Successfully created account.")
                st.session_state.user = new_acc
                st.session_state.logged_in = True
            else:
                if data["users"]:
                    for acc in data["users"]:
                        if acc["email"] == email:
                            cur_acc = acc
                            if check_password_hash(cur_acc["password"], password):
                                st.success("Successfully logged into account.")
                                st.session_state.user = acc
                                st.session_state.logged_in = True
                            else:
                                st.error("Wrong password.")
                        break
                    else:
                        st.error("Email not found. Please sign up.")
                else:
                    st.error("Email not found. Please sign up.")

def log_out():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.success("Successfully signed out of account.")



