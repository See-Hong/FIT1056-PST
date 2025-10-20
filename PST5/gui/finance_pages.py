# gui/finance_pages.py
import streamlit as st
import pandas as pd
from utils.utils import *


def show_finance_page(manager):
    """Renders the UI for all financial operations."""
    st.header("Finance & Payments")

    students = [(student.id, student.name) for student in manager.students]

    if st.session_state.logged_in:
        record_payment(manager, students)

    view_history(manager, students)

def record_payment(manager, students):
    """Records a students payment"""
    st.subheader("Record New Payment")
    with st.form("payment_form"):

        student = student_selectbox("Student Name", students, key="payment-student")
        amount = st.number_input("Payment Amount", min_value=0.01)
        method = st.text_input("Payment Method (e.g., Credit Card, Cash)")

        submitted = st.form_submit_button("Record Payment")
        if submitted:
            student_id = student[0]
            payment = manager.record_payment(student_id, amount, method)
            if payment:
                st.success(f"Payment of {amount} for {student[1]} recorded.")
            else:
                st.error(f"Student not found.")

def view_history(manager, students):
    st.subheader("View Student Payment History")
    student = student_selectbox("Student Name", students, key="payment-history-student")
    if student:
        student_id = student[0]
        history = manager.get_payment_history(student_id)
        if history:
            df = pd.DataFrame(history)
            st.dataframe(df)
        else:
            st.warning("This student has no payment history.")