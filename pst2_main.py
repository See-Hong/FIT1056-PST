import json
from json import JSONDecodeError

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