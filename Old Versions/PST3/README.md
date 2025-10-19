# FIT1056-PST3 (OOP Design)

[![Python](https://img.shields.io/badge/Primary%20Language-Python-blue)](https://www.python.org/)

PST3 is a terminal-based application designed for a music school’s receptionist. It streamlines everyday administrative tasks such as registering new students, enrolling them in courses, and managing teacher and course information.

Built with JSON data storing, and OOP, the system organizes data through classes and functions dedicated to student management, teacher management, and course management. This makes the receptionist’s job easier and reduces the complexity of handling school records manually.

## Project Structure
```
PST3/
|── app/
|   └── schedule.py      # ScheduleManager class
|   └── student.py       # Student class
|   └── teacher.py       # Teacher and Course class
|   └── user.py          # Base User class
|   └── __init__.py
│── data/
│   └── msms.json        # Data files
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
  - ⚠️ **Admin Only**:
    - Remove students
    - List all students
```

🧑‍🏫 Teacher Management
```
- Update teacher information  
  - ⚠️ **Admin Only**:  
    - Register new teachers  
    - Remove teachers  
    - List all teachers  
```

📚 Course Management
```
- Show today's lessons
- List all courses
- Get course lessons
  - ⚠️ **Admin Only**:
    - Add new courses
    - Remove courses
    - Adds lessons to courses
```

📁 Other Functions
```
- Lookup student, teacher, or courses with name/ID
- Log in and out of admin account for admin only features
- Quit and save data
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
  cd PST3
  python main.py
```

2. The program will present the user with a menu
```
===== MSMS v3 (Object-Oriented) =====

----- Student Manager -----
S1. Register New Student
S2. Enrol Existing Student
S3. Disenroll Existing Student
S4. Switch Student Course
S5. Update Student Info
S6. Check-in Student
S7. Check Student Attendance
S8. (Admin) Remove Student
S9. (Admin) List all Students

----- Teacher Manager -----
T1. Update Teacher Info
T2. (Admin) Register New Teacher
T3. (Admin) Remove Teacher
T4. (Admin) List all Teachers

----- Course Manager -----
C1. Today's Lessons
C2. List Courses
C3. Get Lessons
C4. (Admin) Add Course
C5. (Admin) Remove Course
C6. (Admin) Add Lessons

----- Others -----
O1. Lookup Student, Teacher or Course
Login. Log in to admin account
Quit. Quit and Save

```

3. The user can input their choice in the terminal. <br>
   For example, S1 lets you register a new student.
```
Enter your choice: S1
Enter student name: Bob
Enter course ID to enrol in: 101
Enrolled student ID 1 in course ID 101
```

## Dependencies
- [python-dateutil](https://dateutil.readthedocs.io/en/stable/)
