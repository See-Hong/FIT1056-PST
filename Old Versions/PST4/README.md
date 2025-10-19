# FIT1056-PST4 (GUI)

[![Python](https://img.shields.io/badge/Primary%20Language-Python-blue)](https://www.python.org/)

PST4 is a music school management app designed to simplify the administration of students, teachers, and courses.
The system provides an easy-to-use interface for managing day-to-day academic operations, tracking attendance, and student admissions.

Built with Streamlit, the app offers a clean and interactive user experience directly in the browser.
This makes it simple for receptionists and administrative staff to operate without requiring technical expertise, thanks to its clear layout and easy-to-read functions.

## Project Structure
```
PST4/
|── app/
|   └── schedule.py      # ScheduleManager class
|   └── student.py       # Student class
|   └── teacher.py       # Teacher and Course class
|   └── user.py          # Base User class
|   └── __init__.py
│── data/
│   └── msms.json        # Data files
|── gui/
|   └── main_dashboard.py      # Main layout for app
|   └── overview.py            # School statistics page
|   └── student_pages.py       # Student management page
|   └── teacher_pages.py       # Teacher management page
|   └── course_pages.py        # Course management page
|   └── roster_pages.py        # Course roster and attendance page
|   └── __init__.py            
│── main.py              # Program Entry Point
│── .gitignore
│── requirements.txt
```


## Key Features

🧑‍🎓 Student Management
```
- Register new students
- Enrol students into courses
- Disenroll students from courses
- Switch student courses
- Update student information
- Check in students
- Check student attendance
- Remove students
- List all students
```

🧑‍🏫 Teacher Management
```
- Update teacher information  
- Register new teachers  
- Remove teachers  
- List all teachers  
```

📚 Course Management
```
- Show lessons for a day
- List all courses
- Add new courses
- Remove courses
- Get course lessons
- Adds lessons to courses
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/username/FIT1056-PST.git
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
## Usage

1. Run the program
```bash
  cd PST4
  streamlit run main.py
```

2. Open in your browser
Streamlit will automatically open the app in your default browser (usually at http://localhost:8501).

3. Use the navigation sidebar

  ℹ️ Home → Shows basic stats for the music school.
  
  📚 Students Management → Add, update, or remove students, and view their enrolled courses.
  
  🎵 Course Management → Create and manage courses, assign teachers, and view lesson schedules.
  
  👨‍🏫 Teacher Management → Manage teacher information and assign them to courses.
  
  📝 Roster Management → Record student check-in and view lessons for a day.

4. Example workflow

   - Add a new student via the Students page.

   - Add a new course via the Courses page.

   - Enroll the student in a course from the Students page.

   - Record their attendance during lessons.

   - View attendance in the Attendance section.

## Dependencies
Streamlit
 – for the interactive web app interface

pandas
 – for data handling and analysis

python-dateutil
 – for parsing and managing dates