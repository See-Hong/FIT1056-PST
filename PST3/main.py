from app.schedule import ScheduleManager
import datetime as dt
ADMIN_PASSWORD = "admin123"

# Student Functions
def get_student_details(manager, student_id):
    """Prints an existing students details"""
    student = manager.find_by_id(student_id)
    if student:
        print(student)
        print("-" * 20)
    else:
        print(f"Error: Student ID {student_id} not found.")

def list_students(manager):
    """Prints all students in the database."""
    if manager.students:
        print("\n--- Student List ---")
        for student in manager.students:
            get_student_details(manager, student.id)
            print("-" * 20)
    else:
        print("Error: No students found in the system.")

def find_students(manager, term):
    """Finds students by name or id."""
    try:
        term = int(term)
        id_search = True
    except ValueError:
        id_search = False
    print(f"\n--- Finding students matching '{term}' ---")
    # Searches student database for student with the id provided.
    if id_search:
        if manager.find_by_id(term):
            get_student_details(manager, term)
        else:
            print(f"Student ID {term} not found.")
    else:
        # Filters the student database for students with names matching the search term.
        result = [student for student in manager.students() if term.lower() in student.name.lower()]
        for student in result:
            get_student_details(manager, student.id)
        if not result:
            print("No match found.")

def switch_course(manager, student_id, from_course_id, to_course_id):
    """Switches a students course from one to another"""
    old_course = manager.disenroll_student(student_id, from_course_id)
    # Makes sure the student disenrolled is successful before continuing.
    if old_course:
        new_course = manager.enrol_student(student_id, to_course_id)
        # Returns student enrollment status to original if student enrollment is unsuccessful.
        if not new_course:
            manager.enrol_student(student_id, from_course_id)
# Teacher Functions
def find_teachers(manager, term):
    """Finds teachers by name, specialty or id."""
    try:
        term = int(term)
        id_search = True
    except ValueError:
        id_search = False
    print(f"\n--- Finding teacher matching '{term}' ---")
    # Searches teacher database for student with the id provided.
    if id_search:
        if manager.find_by_id(term):
            get_teacher_details(manager, term)
        else:
            print(f"Teacher ID {term} not found.")
    else:
        # Filters the teacher database for teachers with names or specialties matching the search term.
        result = [teacher for teacher in manager.teachers if
                  term.lower() in teacher.name.lower() or term.lower() in teacher.specialty.lower()]
        for teacher in result:
            get_teacher_details(manager, teacher.id)
        if not result:
            print("No match found.")


def get_teacher_details(manager, teacher_id):
    """Prints a teacher's details."""
    teacher = manager.find_by_id(teacher_id, search="teacher")
    if teacher:
        print(teacher)
        print("-" * 20)
    else:
        print(f"Error: Teacher ID {teacher_id} not found.")


def list_teachers(manager):
    """Prints all teachers in the application data."""
    if manager.teachers:
        print("\n--- Teacher List ---")
        for teacher in manager.teachers:
            get_teacher_details(manager, teacher.id)
    else:
        print("Error: No teachers found in the system.")

# Course Functions

def find_courses(manager, term):
    """Finds courses by name, specialty or id."""
    try:
        term = int(term)
        id_search = True
    except ValueError:
        id_search = False
    print(f"\n--- Finding course matching '{term}' ---")
    # Searches system for course with the id provided.
    if id_search:
        if manager.find_by_id(term):
            get_teacher_details(manager, term)
        else:
            print(f"Teacher ID {term} not found.")
    else:
        # Filters the system for courses with names matching the term.
        result = [course for course in manager.courses if term.lower() in course.name.lower()]
        for course in result:
            get_course_details(manager, course.id)
        if not result:
            print("No match found.")


def get_course_details(manager, course_id):
    """Prints a course's details."""
    course = manager.find_by_id(course_id, search="course")
    if course:
        print(course)
        print("-" * 20)
    else:
        print(f"Error: Course ID {course_id} not found.")


def list_courses(manager):
    """Prints all courses in the system."""
    if manager.courses:
        print("\n--- Course List ---")
        for course in manager.courses:
            get_course_details(manager, course.id)
    else:
        print("Error: No teachers found in the system.")

def get_lessons(manager, course_id):
    """Gets the lessons for a course"""
    course = manager.find_by_id(course_id, search="course")
    if course:
        course.get_lessons()
    else:
        print(f"Error: Course ID {course_id} not found.")

def front_desk_daily_roster(manager, day):
    """Displays a pretty table of all lessons on a given day."""
    print(f"\n--- Daily Roster for {day} ---")
    lessons_available = False
    for course in manager.courses:
        for lesson in course.lessons:
            if lesson["day"] == day:
                lessons_available = True
                teacher = manager.find_by_id(course.teacher_id, search="teacher")
                print(f"Course: {course.name}"
                      f"\nTeacher: {teacher.name}"
                      f"\nStart Time: {lesson["start_time"]}"
                      f"\nRoom: {lesson["room"]}")
                print("-" * 20)
    if not lessons_available:
        print(f"No lessons for {day}.")

# Core Helper Functions
def front_desk_register(manager, name, course_id):
    """High-level function to register a new student and enrol them."""
    student = manager.add_student(name)
    # Enrols new student in provided instrument
    enrol = manager.enrol_student(student, course_id)
    if not enrol:
        manager.remove_student(student)
    else:
        print(f"Front Desk: Successfully registered '{name}' and enrolled them in course ID {course_id}.")

def front_desk_lookup(manager, term, search=None):
    """High-level function to search everything."""
    print(f"\n--- Performing lookup for '{term}' ---")
    if search.lower() == "student":
        find_students(manager, term)
    elif search.lower() == "teacher":
        find_teachers(manager, term)
    elif search.lower() == "course":
        find_courses(manager, term)
    else:
        print("Error: Search type invalid.")

def main():
    """Main function to run the MSMS application."""
    manager = ScheduleManager("./data/msms.json")
    is_admin = False
    while True:
        print("\n===== MSMS v3 (Object-Oriented) =====")
        print("\n----- Student Manager -----")
        print("S1. Register New Student")
        print("S2. Enrol Existing Student")
        print("S3. Disenroll Existing Student")
        print("S4. Switch Student Course")
        print("S5. Update Student Info")
        print("S6. Check-in Student")
        print("S7. Check Student Attendance")
        if is_admin:
            print("S8. (Admin) Remove Student")
            print("S9. (Admin) List all Students")

        print("\n----- Teacher Manager -----")
        print("T1. Update Teacher Info")
        if is_admin:
            print("T2. (Admin) Register New Teacher")
            print("T3. (Admin) Remove Teacher")
            print("T4. (Admin) List all Teachers")

        print("\n----- Course Manager -----")
        print("C1. Today's Lessons")
        print("C2. List Courses")
        print("C3. Get Lessons")
        if is_admin:
            print("C4. (Admin) Add Course")
            print("C5. (Admin) Remove Course")
            print("C6. (Admin) Add lessons ")
        print("\n----- Others -----")
        print("O1. Lookup Student, Teacher or Course")
        if is_admin:
            print("Logout. Log out of admin account")
        else:
            print("Login. Log in to admin account")
        print("Quit. Quit and Save")

        choice = input("\nEnter your choice: ").strip().lower()

        if choice == "s1":
            # Registers New Student
            student_name = input("Enter student name: ").strip()
            course_id = int(input("Enter course ID to enrol in: ").strip())
            front_desk_register(manager, student_name, course_id=course_id)
        elif choice == "s2":
            # Enrols Existing Student
            try:
                student_id = int(input("Enter student ID: ").strip())
                course_id = int(input("Enter course ID: ").strip())
                manager.enrol_student(student_id, course_id=course_id)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice == "s3":
            # Disenrolls Existing Student
            try:
                student_id = int(input("Enter student ID: ").strip())
                course_id = int(input("Enter course ID: ").strip())
                manager.disenroll_student(student_id, course_id=course_id)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice == "s4":
            # Switches a Student's Courses
            try:
                student_id = int(input("Enter student ID: ").strip())
                from_course_id = int(input("Enter course ID to disenroll: ").strip())
                to_course_id = int(input("Enter course ID to enrol: ").strip())
                switch_course(manager, student_id, from_course_id=from_course_id, to_course_id=to_course_id)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice == "s5":
            # Updates Student Information
            try:
                student_id = int(input("Enter student ID: ").strip())
                name = input("Enter new student name (Leave it blank to cancel): ").strip()
                kwargs = {"name": name}
                # Removes from kwargs if user left input blank.
                for key in kwargs:
                    if key == "":
                        kwargs = kwargs.pop(key)
                manager.update_information(student_id, type_="student", **kwargs)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice == "s6":
            # Checks In Student
            try:
                student_id = int(input("Enter student ID: ").strip())
                course_id = int(input("Enter course ID: ").strip())
                timestamp = input("Enter check in time. Please use YYYY-MM-DD HH:MM format, default is current time: ")
                manager.check_in(student_id, course_id, timestamp)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice == "s7":
            # Checks Student Attendance
            try:
                student_id = int(input("Enter student ID: ").strip())
                date = input("Enter date to check. Default is current day: ")
                manager.check_attendance(student_id, date=date)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice == "s8" and is_admin:
            # Removes an Existing Student
            try:
                student_id = int(input("Enter student ID: ").strip())
                manager.remove_student(student_id)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice == "s9" and is_admin:
            # Lists all students
            list_students(manager)
        elif choice == "t1":
            # Updates Teacher Info
            try:
                teacher_id = int(input("Enter teacher ID: ").strip())
                name = input("Enter new teacher name (Leave it blank to cancel): ").strip()
                specialty = input("Enter new teacher specialty (Leave it blank to cancel): ").strip()
                kwargs = {
                    "name": name,
                    "specialty": specialty,
                }
                # Removes from kwargs if user left input blank.
                for key in kwargs:
                    if key == "":
                        kwargs = kwargs.pop(key)
                manager.update_information(teacher_id, type_ = "teacher", **kwargs)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice == "t2" and is_admin:
            # Adds a New Teacher
            name = input("Enter teacher name: ").strip()
            specialty = input("Enter teacher specialty: ").strip()
            manager.add_teacher(name=name, specialty=specialty)
        elif choice == "t3" and is_admin:
            # Removes an Existing Teacher
            try:
                teacher_id = int(input("Enter teacher ID: ").strip())
                manager.remove_teacher(teacher_id)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice == "t4" and is_admin:
            # Lists all teachers
            list_teachers(manager)
        elif choice == "c1":
            # Shows all lessons for the day.
            day = dt.datetime.today().strftime("%A")
            front_desk_daily_roster(manager, day=day)
        elif choice == "c2":
            # Lists all courses
            list_courses(manager)
        elif choice == "c3":
            # Gets lessons for a course
            try:
                course_id = int(input("Enter course ID: ").strip())
                get_lessons(manager, course_id)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice == "c4" and is_admin:
            # Adds a new course
            try:
                name = input("Enter course name: ").strip()
                instrument = input("Enter course instrument: ").strip()
                teacher_id = int(input("Enter course teacher ID: ").strip())
                manager.add_course(name=name, instrument=instrument, teacher_id=teacher_id)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice == "c5" and is_admin:
            # Removes an existing course
            try:
                course_id = int(input("Enter course ID: ").strip())
                manager.remove_course(course_id)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice == "c6" and is_admin:
            # Add a lesson to a course
            try:
                course_id = input("Enter course ID: ").strip()
                day = input("Enter lesson day: ").strip()
                start_time = input("Enter lesson start time: ").strip()
                room = input("Enter lesson location: ").strip()
                manager.add_lesson(course_id, lesson_day=day, start_time=start_time, room=room)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice == "o1":
            # Searches for students, teachers or courses.
            choice = input("Enter search type (Student/Teacher/Course): ").strip()
            term = input("Enter search term: ").strip().lower()
            front_desk_lookup(manager, term, search=choice)
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
            print("Exiting School Management Program.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

