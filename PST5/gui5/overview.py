import streamlit as st

def overview_page(manager):
    with st.container(border=True, key="test"):
        st.header("Music School Statistics")
        st.divider()
        st.markdown("""<style> .st-key-test {
             background-color: gray
             }
             """, unsafe_allow_html=True)
        st.markdown(f"<h3> Number of students: {len(manager.students)} </h3>",unsafe_allow_html=True)
        st.markdown(f"<h3> Number of teachers: {len(manager.teachers)} </h3>",unsafe_allow_html=True)
        st.markdown(f"<h3> Number of courses: {len(manager.courses)} </h3>",unsafe_allow_html=True)