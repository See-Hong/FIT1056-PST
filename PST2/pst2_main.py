import json
from json import JSONDecodeError
import datetime as dt


# JSON data management
app_data = {}
DATA_FILE = "msms.json"
def load_data(path):
    """Loads all application data from a JSON file."""
    global app_data
    try:
        with open(file=path, mode="r") as file:
            app_data = json.load(file)
            print("Data loaded successfully.")
    except (FileNotFoundError, JSONDecodeError):
        print("Data file error. Initializing with default structure.")
        app_data = {
            "students": [],
            "teachers": [],
            "attendance": [],
            "next_student_id": 1,
            "next_teacher_id": 1
        }
        with open(file=path, mode="w") as file:
            json.dump(app_data, fp=file, indent=4)

def save_data(path):
    """Save all application data to a JSON file"""
    with open(file=path, mode="w") as file:
        json.dump(app_data, fp=file, indent=4)
    print("Data saved successfully.")

# Core Helper Functions
def add_teacher(name, specialty):
    """Adds a teacher to the application data."""

    new_teacher = {
        "name": name,
        "id": app_data["next_teacher_id"],
        "specialty": specialty,
    }
    app_data["teachers"].append(new_teacher)
    app_data["next_teacher_id"] += 1

def update_teacher(teacher_id, **kwargs):
    """Updates an existing teachers information."""
    for teacher in app_data["teachers"]:
        if teacher["id"] == teacher_id:
            # Executes if user has provided items to change.
            if kwargs:
                teacher.update(kwargs)
                print(f"Teacher ID {teacher_id} updated.")
                print("-" * 20)
                for data in kwargs:
                    print(f"{data.capitalize()} : {kwargs[data]}")
                print("-" * 20)
                return
            else:
                print(f"No data for teacher ID {teacher_id} has been changed")
    print(f"Teacher ID {teacher_id} not found.")

def remove_teacher(teacher_id):
    """Removes an existing teacher from the application data."""
    for teacher in app_data["teachers"]:
        if teacher["id"] == teacher_id:
            app_data["teachers"].remove(teacher)
            print(f"Teacher ID {teacher_id} has been removed.")
            return
    print(f"Teacher ID {teacher_id} not found.")

def update_student(student_id, **kwargs):
    """Updates an existing students information."""
    for student in app_data["teachers"]:
        if student["id"] == student_id:
            # Executes if user has provided items to change.
            if kwargs:
                student.update(kwargs)
                print(f"Student ID {student_id} updated.")
                print("-" * 20)
                for data in kwargs:
                    print(f"{data.capitalize()} : {kwargs[data]}")
                print("-" * 20)
                return
            else:
                print(f"No data for student ID {student_id} has been changed")
    print(f"Student ID {student_id} not found.")

def remove_student(student_id):
    """Removes an existing student from the application data."""
    for student in app_data["teachers"]:
        if student["id"] == student_id:
            app_data["students"].remove(student)
            print(f"Student ID {student_id} has been removed.")
            return
    print(f"Student ID {student_id} not found.")

def check_in(student_id, course_id, timestamp=None):
    """Records a student's attendance for a course."""
    if not timestamp:
        timestamp = dt.datetime.now()
    else:
        try:
            timestamp = dt.datetime.strptime(timestamp, "%Y-%m-%d %H:%M")
        except ValueError:
            print("An error occurred, using current date and time.")
            timestamp = dt.datetime.now()
    for student in app_data["students"]:
        if student["id"] == student_id:
            if course_id in student["courses"]:
                new_record = {
                    "id": student_id,
                    "course_id": course_id,
                    "timestamp": timestamp
                }
                app_data["attendance"].append(new_record)
                return
            else:
                print(f"Student ID {student_id} is not enrolled in course ID {course_id}.")
                return
    print(f"Student ID {student_id} not found.")

def check_attendance(student_id, date=None):
    """Checks a student's attendance for a certain day."""
    check_date = dt.datetime.now()
    # Formats the date given. If an error occurs, the current date is used.
    if date:
        try:
            check_date = dt.datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("Error: Date provided invalid. Please use the YYYY-MM-DD format.")
            print("Using current date.")
    for student in app_data["students"]:
        if student["id"] == student_id:
            print("-" * 15)
            print(f"Attendance for Student ID {student_id} for {date}")
            print("-" * 15)
            record_found = False
            for record in student["attendance"]:
                # Checks each attendance record for the same date.
                if record["timestamp"].date() == check_date.date():
                    record_found = True
                    print(f"Course ID: {record["course_id"]}")
                    print(f"Timestamp: {record["timestamp"].strftime("%H:%M")}")
                    print("-" * 15)
            if not record_found:
                print(f"No records found for student ID {student_id} at {date}.")
    print(f"Student ID {student_id} not found.")

def print_student_card(student_id):
    """Creates a text file badge for a student."""
    for student in app_data["students"]:
        if student["id"] == student_id:
            sel_student = student
            file_path = f"{student_id}_card.txt"
            # Creates file if file doesn't exist. If it exists, clear the file.
            with open(file=file_path, mode="w") as file:
                file.write("")
            # Writes the student details into the file
            with open(file=file_path, mode="a") as file:
                file.write("========================\n")
                file.write(f"  MUSIC SCHOOL ID BADGE\n")
                file.write("========================\n")
                file.write(f"ID: {sel_student['id']}\n")
                file.write(f"Name: {sel_student['name']}\n")
                file.write(f"Enrolled In: {', '.join(sel_student.get('enrolled_in', []))}\n")
            print(f"Printed student card to {file_path}.")
    print(f"Student ID {student_id} not found.")