import streamlit as st

def overview_page(manager):
    with st.container(border=True, key="test"):
        st.header("Music School Statistics")
        st.divider()
        st.markdown("""<style> .st-key-test {
             background-color: gray
             }
             """, unsafe_allow_html=True)