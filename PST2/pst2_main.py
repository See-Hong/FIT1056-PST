import json
from json import JSONDecodeError
import datetime as dt

# JSON data management
app_data = {}
DATA_FILE = "msms.json"
ADMIN_PASSWORD = "Admin123"
def load_data(path=DATA_FILE):
    """Loads all application data from a JSON file."""
    global app_data
    try:
        with open(file=path, mode="r") as file:
            app_data = json.load(file)
            print("Data loaded successfully.")
    except (FileNotFoundError, JSONDecodeError):
        print("Data File Error: Initializing with default structure.")
        app_data = {
            "students": [],
            "teachers": [],
            "attendance": [],
            "next_student_id": 1,
            "next_teacher_id": 1
        }
        with open(file=path, mode="w") as file:
            json.dump(app_data, fp=file, indent=4)

def save_data(path=DATA_FILE):
    """Save all application data to a JSON file"""
    with open(file=path, mode="w") as file:
        json.dump(app_data, fp=file, indent=4)
    print("Data saved successfully.")

## Core Helper Functions

# Student Functions
def get_student_details(student_id):
    """Prints an existing students details"""
    student = find_by_id(student_id)
    if student:
        print("-"* 15)
        print(f"ID: {student["id"]}")
        print(f"NAME: {student["name"]}")
        print(f"COURSES {"|".join(student["courses"])}")
        print("-" * 15)
    else:
        print(f"Error: Student ID {student_id} not found.")


def update_student(student_id, **kwargs):
    """Updates an existing students information."""
    student = find_by_id(student_id)
    if student:
        # Checks kwargs for empty inputs.
        change_data = {}
        for data in kwargs:
            if kwargs[data] != "":
                change_data.update({
                    data: kwargs[data]
                }
                )
        # Executes if user has provided items to change.
        if change_data:
            student.update(change_data)

            # Output for user
            print(f"Student ID {student_id} updated.")
            print("-" * 20)
            for data in change_data:
                print(f"{data.capitalize()} : {change_data[data]}")
            print("-" * 20)
            save_data()
        else:
            print(f"No data for student ID {student_id} has been changed")
    else:
        print(f"Error: Student ID {student_id} not found.")

def remove_student(student_id):
    """Removes an existing student from the application data."""
    student = find_by_id(student_id)
    if student:
        app_data["students"].remove(student)
        print(f"Student ID {student_id} has been removed.")
        save_data()
    else:
        print(f"Error: Student ID {student_id} not found.")

def find_students(term):
    """Finds students by name or id."""
    try:
        term = int(term)
        id_search = True
    except ValueError:
        id_search = False
    print(f"\n--- Finding students matching '{term}' ---")
    # Searches student database for student with the id provided.
    if id_search:
        if find_by_id(term):
            get_student_details(term)
        else:
            print(f"Student ID {term} not found.")
    else:
        # Filters the student database for students with names matching the search term.
        result = [student for student in app_data["students"] if term.lower() in student["name"].lower()]
        for student in result:
            get_student_details(student["id"])
        if not result:
            print("No match found.")

def list_students():
    """Prints all students in the database."""
    if app_data["students"]:
        print("\n--- Student List ---")
        for student in app_data["students"]:
            get_student_details(student["id"])
    else:
        print("Error: No students found in the system.")

def check_in(student_id, course, timestamp=None):
    """Records a student's attendance for a course."""
    if not timestamp:
        timestamp = dt.datetime.now().isoformat(timespec="minutes")
    else:
        try:
            timestamp = dt.datetime.strptime(timestamp, "%Y-%m-%d %H:%M").isoformat(timespec="minutes")
        except ValueError:
            print("An error occurred, using current date and time.")
            timestamp = dt.datetime.now().isoformat(timespec="minutes")
    student = find_by_id(student_id)
    if student:
        if course.lower() in student["courses"]:
            new_record = {
                "id": student_id,
                "course": course.lower(),
                "timestamp": timestamp
            }
            app_data["attendance"].append(new_record)
            print(f"Checked in student ID {student_id} in {course} at {timestamp}.")
            save_data()
        else:
            print(f"Error: Student ID {student_id} is not enrolled in {course}.")
    else:
        print(f"Error: Student ID {student_id} not found.")

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
    student = find_by_id(student_id)
    # Checks if the student exist before continuing.
    if student:
        record_list = []
        # Gets all the records for a student.
        for record in app_data["attendance"]:
            if record["id"] == student_id:
                record_list.append(record)
        if record_list:
            print("-" * 15)
            print(f"Attendance for Student ID {student_id} for {date}")
            print("-" * 15)
            record_found = False
            # Checks each attendance record for the same date.
            for record in record_list:
                record_date = dt.datetime.fromisoformat(record["timestamp"])
                if record_date.date() == check_date.date():
                    record_found = True
                    print(f"Course ID: {record["course"]}")
                    print(f"Timestamp: {record_date.strftime("%H:%M")}")
                    print("-" * 15)
            if not record_found:
                print(f"No records found for student ID {student_id} at {date}.")
        else:
            print(f"No records found for student ID {student_id}.")
    else:
        print(f"Error: Student ID {student_id} not found.")

def print_student_card(student_id):
    """Creates a text file badge for a student."""
    student = find_by_id(student_id)
    if student:
        file_path = f"{student_id}_card.txt"
        # Creates file if file doesn't exist. If it exists, clear the file.
        with open(file=file_path, mode="w") as file:
            file.write("")
        # Writes the student details into the file
        with open(file=file_path, mode="a") as file:
            file.write("========================\n")
            file.write(f"  MUSIC SCHOOL ID BADGE\n")
            file.write("========================\n")
            file.write(f"ID: {student['id']}\n")
            file.write(f"Name: {student['name']}\n")
            file.write(f"Enrolled In: {', '.join(student["courses"])}\n")
        print(f"Printed student card to {file_path}.")
    else:
        print(f"Error: Student ID {student_id} not found.")

# Teacher Functions
def get_teacher_details(teacher_id):
    """Prints a teacher's details."""
    teacher = find_by_id(teacher_id, search="teacher")
    if teacher:
        print("-" * 15)
        print(f"ID: {teacher["id"]}")
        print(f"NAME: {teacher["name"]}")
        print(f"SPECIALTY: {teacher["specialty"]}")
        print("-" * 15)
    else:
        print(f"Error: Teacher ID {teacher_id} not found.")

def add_teacher(name, specialty):
    """Adds a teacher to the application data."""
    new_teacher = {
        "name": name,
        "id": app_data["next_teacher_id"],
        "specialty": specialty,
    }
    app_data["teachers"].append(new_teacher)
    app_data["next_teacher_id"] += 1
    save_data()

def update_teacher(teacher_id, **kwargs):
    """Updates an existing teachers information."""
    teacher = find_by_id(teacher_id, search="teacher")
    if teacher:
        # Checks kwargs for empty inputs.
        change_data = {}
        for data in kwargs:
            if kwargs[data] != "":
                change_data.update({
                    data: kwargs[data]
                }
                )

        # Executes if user has provided items to change.
        if change_data:
            teacher.update(kwargs)

            # Output for user
            print(f"Teacher ID {teacher_id} updated.")
            print("-" * 20)
            for data in change_data:
                print(f"{data.capitalize()} : {change_data[data]}")
            print("-" * 20)
            save_data()
        else:
            print(f"No data for teacher ID {teacher_id} has been changed")
    else:
        print(f"Error: Teacher ID {teacher_id} not found.")

def remove_teacher(teacher_id):
    """Removes an existing teacher from the application data."""
    teacher = find_by_id(teacher_id, search="teacher")
    if teacher:
        app_data["teachers"].remove(teacher)
        print(f"Teacher ID {teacher_id} has been removed.")
        save_data()
    else:
        print(f"Error: Teacher ID {teacher_id} not found.")

def find_teachers(term):
    """Finds teachers by name, specialty or id."""
    try:
        term = int(term)
        id_search = True
    except ValueError:
        id_search = False
    print(f"\n--- Finding teacher matching '{term}' ---")
    # Searches teacher database for student with the id provided.
    if id_search:
        if find_by_id(term):
            get_teacher_details(term)
        else:
            print(f"Teacher ID {term} not found.")
    else:
        # Filters the teacher database for teachers with names or specialties matching the search term.
        result = [teacher for teacher in app_data["teachers"] if term.lower() in teacher["name"].lower() or term.lower() in teacher["specialty"].lower()]
        for teacher in result:
            get_teacher_details(teacher["id"])
        if not result:
            print("No match found.")

def list_teachers():
    """Prints all teachers in the application data."""
    if app_data["teachers"]:
        print("\n--- Teacher List ---")
        for teacher in app_data["teachers"]:
            get_teacher_details(teacher["id"])
    else:
        print("Error: No teachers found in the system.")

# Front Desk Functions

def front_desk_register(name, course):
    """High-level function to register a new student and enrol them."""
    global app_data
    new_student = {
        "name": name,
        "id": app_data["next_student_id"],
        "courses": [],
    }
    app_data["students"].append(new_student)
    app_data["next_student_id"] += 1
    # Enrols new student in provided instrument
    front_desk_enrol(new_student["id"], course=course)
    save_data()
    print(f"Front Desk: Successfully registered '{name}' and enrolled them in '{course}'.")


def front_desk_enrol(student_id, course):
    """High-level function to enrol an existing student in a course."""
    student = find_by_id(student_id)
    if student:
        # Checks if student is already enrolled in an instrument.
        for course_name in student["courses"]:
            if course.lower() == course_name.lower():
                print(f"Error: Student ID {student_id} already enrolled in {course}.")
        # Runs if student is not already enrolled in the instrument.
        else:
            student["courses"].append(course.lower())
            save_data()
            print(f"Front Desk: Enrolled student ID {student_id} in '{course}'.")
    else:
        print(f"Error: Student ID {student_id} not found.")

def front_desk_unenroll(student_id):
    """High-level function to unenroll an existing student in a course."""
    student = find_by_id(student_id)
    if student:
        enrolled_instruments = student["courses"]
        if enrolled_instruments:
            # Lists instruments the current student is enrolled in and waits for user input.
            print(f"The current student is enrolled in {"|".join(enrolled_instruments)}")
            instrument = input("Please select which instrument to unenroll the student in.\n")
            # Checks if student is enrolled in the instrument.
            try:
                enrolled_instruments.remove(instrument)
                student["courses"] = enrolled_instruments
                print(f"Front Desk: Unenrolled student {student_id} in {instrument}.")
                save_data()
            except ValueError:
                print(f"Error: The current student is not enrolled in {instrument}.")
        else:
            print("The current student is not enrolled in any instruments.")
    else:
        print(f"Error: Student ID {student_id} not found.")

def front_desk_lookup(term, search=None):
    """High-level function to search everything."""
    print(f"\n--- Performing lookup for '{term}' ---")
    if search.lower() == "student":
        find_students(term)
    elif search.lower() == "teacher":
        find_teachers(term)
    elif search.lower() == "both":
        find_students(term)
        find_teachers(term)
    else:
        print("Error: Search type invalid.")


def find_by_id(_id, search="student"):
    """Finds a student or teacher with the provided id. Default is student search."""
    if search == "student":
        for student in app_data["students"]:
            if student["id"] == _id:
                return student
        return None
    elif search == "teacher":
        for teacher in app_data["teachers"]:
            if teacher["id"] == _id:
                return teacher
        return None
    else:
        raise "Error: Search type invalid."

def main():
    """Runs the main interactive menu for the receptionist."""
    load_data("msms.json")
    is_admin = False
    while True:
        print("\n===== MSMS v2 (Persistent) =====")
        print("\n----- Student Manager -----")
        print("S1. Register New Student")
        print("S2. Enrol Existing Student")
        print("S3. Unenroll Existing Student")
        print("S4. Update Student Info")
        print("S5. Check-in Student")
        print("S6. Check Student Attendance")
        print("S7. Print Student Card")
        if is_admin:
            print("S8. (Admin) Remove Student")
            print("S9. (Admin) List all Students")

        print("\n----- Teacher Manager -----")
        print("T1. Update Teacher Info")
        if is_admin:
            print("T2. (Admin) Register New Teacher")
            print("T3. (Admin) Remove Teacher")
            print("T4. (Admin) List all Teachers")

        print("\n----- Others -----")
        print("O1. Lookup Student or Teacher")
        if is_admin:
            print("Logout. Log out of admin account")
        else:
            print("Login. Log in to admin account")
        print("Quit. Quit and Save")

        choice = input("\nEnter your choice: ").strip().lower()

        if choice == "s1":
            # Registers New Student
            student_name = input("Enter student name: ").strip()
            course = input("Enter course to enrol in: ").strip()
            front_desk_register(student_name, course=course)
        elif choice == "s2":
            # Enrols Existing Student
            try:
                student_id = int(input("Enter student ID: ").strip())
                course = input("Enter course to enrol in: ").strip()
                front_desk_enrol(student_id, course=course)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice == "s3":
            # Unenrolls Existing Student
            try:
                student_id = int(input("Enter student ID: ").strip())
                front_desk_unenroll(student_id)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice == "s4":
            # Updates Student Information
            try:
                student_id = int(input("Enter student ID: ").strip())
                name = input("Enter new student name (Leave it blank to cancel): ").strip()
                update_student(student_id, name=name)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice == "s5":
            # Checks In Student
            try:
                student_id = int(input("Enter student ID: ").strip())
                course = input("Enter course name: ").strip()
                timestamp = input("Enter check in time. Please use YYYY-MM-DD HH:MM format, default is current time: ")
                check_in(student_id, course, timestamp)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice == "s6":
            # Checks Student Attendance
            try:
                student_id = int(input("Enter student ID: ").strip())
                date = input("Enter date to check. Please use YYYY-MM-DD format, default is current day: ")
                check_attendance(student_id, date=date)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice == "s7":
            # Prints Student Card into Text File
            try:
                student_id = int(input("Enter student ID: ").strip())
                print_student_card(student_id)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice == "s8" and is_admin:
            # Removes an Existing Student
            try:
                student_id = int(input("Enter student ID: ").strip())
                remove_student(student_id)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice == "s9" and is_admin:
            # Lists all students
            list_students()
        elif choice == "t1":
            # Updates Teacher Info
            try:
                teacher_id = int(input("Enter teacher ID: ").strip())
                name = input("Enter new teacher name (Leave it blank to cancel): ").strip()
                specialty = input("Enter new teacher specialty (Leave it blank to cancel): ").strip()
                update_teacher(teacher_id, name=name, specialty=specialty)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice == "t2" and is_admin:
            # Adds a New Teacher
            name = input("Enter teacher name: ").strip()
            specialty = input("Enter teacher specialty: ").strip()
            add_teacher(name=name, specialty=specialty)
        elif choice == "t3" and is_admin:
            # Removes an Existing Teacher
            try:
                teacher_id = int(input("Enter teacher ID: ").strip())
                remove_teacher(teacher_id)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice == "t4" and is_admin:
            # Lists all teachers
            list_teachers()
        elif choice == "o1":
            # Searches for students or teachers.
            choice = input("Enter search type (Student/Teacher/Both): ").strip()
            term = input("Enter search term: ").strip()
            front_desk_lookup(term, search=choice)
        # Log Out of Admin Account
        elif choice == "logout" and is_admin:
            is_admin = False
            print("Logged out of admin account.")
        elif choice == "login" and not is_admin:
            # Log Into Admin Account
            password = input("Please enter admin password: ").strip()
            if password == ADMIN_PASSWORD:
                is_admin = True
            else:
                print("Error: Password incorrect.")
        elif choice == "quit":
            # Exit Program
            save_data()
            print("Exiting School Management Program.")
            break
        else:
            print("Invalid choice. Please try again.")

# Program Start
if __name__ == "__main__":
    main()
