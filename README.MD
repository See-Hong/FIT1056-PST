# FIT1056-PST5 (Quality Assurance)

[![Python](https://img.shields.io/badge/Primary%20Language-Python-blue)](https://www.python.org/)

PST5 is a music school management system designed to simplify the administration of students, teachers, courses, and payments.
It provides a modern, browser-based interface for handling daily academic and financial operations efficiently.

Built with Streamlit, the app offers an intuitive and interactive user experience, making it easy for staff to manage student admissions,
attendance tracking, payment records, and school statistics — all without requiring technical expertise.

The system also includes account login, activity logging, and automated backups to ensure data security and reliability.
In addition, unit testing is implemented to maintain system stability and ensure consistent performance across all modules.

## Project Structure
```
PST5/
|── app/
|   └── schedule.py      # ScheduleManager class
|   └── student.py       # Student class
|   └── teacher.py       # Teacher and Course class
|   └── user.py          # Base User class
|   └── admin_utils.py   # Admin utils
|   └── __init__.py
│── data/
│   └── msms.json        # Data files
│   └── account.json     # Account data files
│   └── backups/         # Backups directory
│── assets/              # System files
|── gui/
|   └── main_dashboard.py      # Main layout for app
|   └── overview.py            # School statistics page
|   └── student_pages.py       # Student management page
|   └── teacher_pages.py       # Teacher management page
|   └── course_pages.py        # Course management page
|   └── roster_pages.py        # Course roster and attendance page
|   └── roster_pages.py        # Student payments page
|   └── __init__.py
|── tests/
|   └── test_schedule_manager.py     # Unit testing files for ScheduleManager
|── utils/
|   └── utils.py         # Helper utilities for web app
|   └── __init__.py
│── main.py              # Program Entry Point
│── .gitignore
|── msms.log             # Program log file
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
- Print attendance report
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

💰 Payment Management
```
- Add student payment
- Check student payment history
- Print payment report
```

🧔‍♂️ Administrative Functions
```
- System backups
- Action logging
```

📰 Other Functions
```
- Account registration and login
- Restricted access for not logged in users
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
  cd PST5
  streamlit run main.py
```

2. Open in your browser
Streamlit will automatically open the app in your default browser (usually at http://localhost:8501).

3. Use the navigation sidebar

  ℹ️ Home → Shows statistics for the music school.
  
  📚 Students Management → Add, update, or remove students, and view their enrolled courses.
  
  🎵 Course Management → Create and manage courses, assign teachers, and view lesson schedules.
  
  👨‍🏫 Teacher Management → Manage teacher information and assign them to courses.
  
  📝 Roster Management → Record student check-in and view lessons for a day.

  💸 Payments → Record student payments and check payment history.

4. Example workflow

   - Add a new student via the Students page.

   - Add a new course via the Courses page.

   - Enroll the student in a course from the Students page.

   - Record their attendance during lessons.

   - View attendance in the Attendance section.
  
   - Record student payment in the Payment section.

5. Unit testing
   ```bash
     cd PST5
     pytest
   ```
   The results of the unit tests are outputted in the terminal.

## Dependencies

- **Streamlit** – Interactive web app interface  
- **pandas** – Data handling and analysis  
- **python-dateutil** – Date parsing and management  
- **Werkzeug** – Password hashing for accounts  
- **pytest** – Unit testing framework  
- **matplotlib** – Data visualization and graphing  
