import json
from json import JSONDecodeError


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