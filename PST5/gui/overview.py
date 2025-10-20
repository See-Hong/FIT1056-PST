import streamlit as st
import matplotlib.pyplot as plt

def overview_page(manager):
    instruments = [course.instrument for course in manager.courses]
    instruments = list(set(instruments))

    with st.container(border=True, key="overview1"):
        st.header("Music School Statistics")
        st.divider()
        col1, col2, col3 = st.columns(spec=3, border=True)
        with col1:
            st.subheader("Metrics")
            st.divider()
            st.markdown(f"<h4> Students: {len(manager.students)} </h4>",unsafe_allow_html=True)
            st.markdown(f"<h4> Teachers: {len(manager.teachers)} </h4>",unsafe_allow_html=True)
            st.markdown(f"<h4> Courses: {len(manager.courses)} </h4>",unsafe_allow_html=True)

        with col2:
            st.subheader("Available Courses")
            st.divider()
            for item in instruments:
                st.markdown(f"<h4>- {item}</h4>", unsafe_allow_html=True)

        with col3:
            st.subheader("Course Enrollment Distribution")
            st.divider()
            course_data = [(course.name,len(course.enrolled_students)) for course in manager.courses]
            fig, ax = plt.subplots()
            rgb = (14, 17, 23)
            converted_rgb = tuple(val / 255 for val in rgb)
            fig.set_facecolor(converted_rgb)
            ax.pie(
                x=[course[1] for course in course_data],
                labels=[course[0] for course in course_data],
                startangle=90,
                textprops={'color': 'white'}
            )

            st.pyplot(fig)


        with st.container(border=True, key="reports"):
            st.subheader("Print reports")
            option = st.radio("Report Type", options=["Attendance", "Finance"], key="report_option")
            if st.button("Generate Report", key="generate_report"):
                with open(manager.export_report(kind=option.lower()), "r") as file:
                    st.download_button("Download Report", file, file_name="Report.csv", key="report_download")