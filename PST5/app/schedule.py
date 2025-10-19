from app.student import StudentUser
from app.teacher import  TeacherUser, Course
import json
import datetime as dt
from dateutil import parser
import difflib
import pandas as pd
import csv


class ScheduleManager:

    def __init__(self, file_path="PST5/data/msms.json"):
        self.students = []
        self.teachers = []
        self.courses = []
        self.attendance_log = []
        self.finance_log = []
        self.next_student_id = 1
        self.next_teacher_id = 1
        self.next_course_id = 101
        self.next_lesson_id = 1
        self.next_finance_id = 1
        self.file_path = file_path
        self._load_data()

    # Data management functions.

    def _load_data(self):
        try:
            with open(file=self.file_path, mode="r") as file:
                data = json.load(file)
                self.init_data(data)
        except (FileNotFoundError, json.JSONDecodeError):
            with open(file=self.file_path, mode="w") as file:
                print("No data found. Creating new data file.")

    def _save_data(self):
        app_data = {
            "students": [student.__dict__ for student in self.students],
            "teachers": [teacher.__dict__ for teacher in self.teachers],
            "courses": [course.__dict__ for course in self.courses],
            "attendance": self.attendance_log,
            "finances": self.finance_log,
        }
        with open(file=self.file_path, mode="w") as file:
            json.dump(app_data, fp=file, indent=5)

    # Data management helper functions.

    def init_data(self, data):
        """Initialize all data"""
        self.load_students(data["students"])
        self.load_teachers(data["teachers"])
        self.load_courses(data["courses"])
        for record in data.get("attendance", []):
            self.attendance_log.append(record)
        for record in data.get("finances", []):
            self.finance_log.append(record)

        # Initializes all data from the json
        # Checks if the current data file contains id counters.
        # If not, sets them to the next number from the highest id.
        # If there is no data for the counters, sets it to the default value.
        self.next_student_id = max(student.id for student in self.students) + 1 if self.students else 1
        self.next_teacher_id = max(teacher.id for teacher in self.teachers) + 1 if self.teachers else 1
        self.next_course_id = max(course.id for course in self.courses) + 1 if self.courses else 101  # Counter for lessons
        lesson_list = [course.lessons for course in self.courses]
        all_lessons = []
        # Flatten lesson_list
        for element in lesson_list:
            if type(element) == list:
                for lesson in element:
                    all_lessons.append(lesson)
            else:
                all_lessons.append(element)
        self.next_lesson_id = data.get("next_lesson_id") or (
                    max(lesson["lesson_id"] for lesson in all_lessons) + 1) if all_lessons else 1
        self.next_lesson_id = max(record["id"] for record in self.finance_log) + 1 if self.finance_log else 1

    def load_students(self, data):
        """Initializes student objects with the given data."""
        for student in data:
            new_student = StudentUser(
                student_id=student["id"],
                name=student["name"]
            )
            new_student.enrolled_courses = student.get("enrolled_courses", [])
            self.students.append(new_student)

    def load_teachers(self, data):
        """Initializes teacher objects with the given data."""
        for teacher in data:
            new_teacher = TeacherUser(
                teacher_id=teacher["id"],
                name=teacher["name"],
                specialty=teacher["specialty"]
            )
            self.teachers.append(new_teacher)

    def load_courses(self, data):
        """Initializes course objects with the given data."""
        for course in data:
            new_course = Course(
                course_id=course["id"],
                name=course["name"],
                instrument=course["instrument"],
                teacher_id=course["teacher_id"],
            )
            new_course.enrolled_students = course.get("enrolled_students", [])
            new_course.lessons = course.get("lessons", [])
            self.courses.append(new_course)

    # Student Functions

    def add_student(self, name):
        """Adds a student to the system."""
        new_student = StudentUser(
            name = name,
            student_id = self.next_student_id,
        )
        self.students.append(new_student)
        print(f"New student ID {self.next_student_id} created.")
        self.next_student_id += 1
        self._save_data()
        return new_student.id

    def remove_student(self, student_id):
        """Removes a student from the system."""
        student = self.find_by_id(student_id)
        if student:
            self.students.remove(student)
            for course in student.enrolled_courses:
                sel_course = self.find_by_id(course, search="course")
                sel_course.enrolled_students.remove(student.id)
            self._save_data()
            print(f"Student ID {student_id} removed.")
            return True
        else:
            print(f"Student ID {student_id} not found.")
            return False

    def enrol_student(self, student_id, course_id):
        """Enrols a student into a course"""
        student = self.find_by_id(student_id)
        course = self.find_by_id(course_id, search="course")
        if not (student and course):
            print("Student or course not found.")
            return False
        if course_id in student.enrolled_courses or student_id in course.enrolled_students:
            print(f"Student ID {student_id} already enrolled in course ID {course_id}.")
            return False
        student.enrolled_courses.append(course_id)
        course.enrolled_students.append(student_id)
        self._save_data()
        print(f"Student ID {student_id} enrolled in course ID {course_id}")
        return True

    def disenroll_student(self, student_id, course_id):
        """Disenroll student in a course."""
        student = self.find_by_id(student_id)
        course = self.find_by_id(course_id, search="course")
        if not (student and course):
            print("Student or course not found.")
            return False
        if course_id in student.enrolled_courses or student_id in course.enrolled_students:
            student.enrolled_courses.remove(course_id)
            course.enrolled_students.remove(student_id)
            self._save_data()
            print(f"Student ID {student_id} disenrolled in course {course_id}.")
            return True
        print(f"Student ID {student_id} not enrolled in course ID {course_id}.")
        return False

    def check_in(self, student_id, course_id, timestamp):
        """Records a student's attendance for a course."""
        if not timestamp:
            timestamp = dt.datetime.now().isoformat()
        elif isinstance(timestamp, dt.datetime):
            timestamp = timestamp.isoformat()
        else:
            try:
                timestamp = parser.parse(timestamp).isoformat()
            except ValueError:
                print("An error occurred, using current date and time.")
                timestamp = dt.datetime.now().isoformat()

        student = self.find_by_id(student_id)
        course = self.find_by_id(course_id, search="course")

        if not student or not course:
            print("Student or course not found.")
            return False

        if course.id in student.enrolled_courses:
            new_record = {
                "student_id": student.id,
                "course_id": course.id,
                "timestamp": timestamp
            }
            if new_record in self.attendance_log:
                print("Error: Duplicate record found")
                return False
            self.attendance_log.append(new_record)
            self._save_data()
            print(f"Student {student.name} checked into {course.name}")
            return True
        print(f"Student ID {student_id} not enrolled in course ID {course_id}")
        return False

    def check_attendance(self, student_id, date=None):
        """Checks a student's attendance for a certain day."""
        check_date = dt.datetime.now()
        # Formats the date given. If an error occurs, the current date is used.
        if date:
            try:
                check_date = parser.parse(date)
            except ValueError:
                print("Error: Date invalid")
                print("Using current date.")
        student = self.find_by_id(student_id)
        # Checks if the student exist before continuing.
        if student:
            record_list = []
            # Gets all the records for a student.
            for record in self.attendance_log:
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
            print(f"Student ID {student_id} not found.")

    def get_student_details(self, student_id):
        """Prints an existing students details"""
        student = self.find_by_id(student_id)
        if student:
            print(student)
            print("-" * 20)
        else:
            print(f"Error: Student ID {student_id} not found.")

    def list_students(self):
        """Prints all students in the database."""
        if self.students:
            print("\n--- Student List ---")
            for student in self.students:
                self.get_student_details(student.id)
                print("-" * 20)
        else:
            print("Error: No students found in the system.")

    def find_students(self, term):
        """Finds students by name or id."""
        try:
            term = int(term)
            id_search = True
        except ValueError:
            id_search = False
        print(f"\n--- Finding students matching '{term}' ---")
        # Searches student database for student with the id provided.
        if id_search:
            if self.find_by_id(term):
                self.get_student_details(term)
            else:
                print(f"Student ID {term} not found.")
        else:
            # Filters the student database for students with names matching the search term.
            result = [student for student in self.students if term.lower() in student.name.lower()]
            for student in result:
                self.get_student_details(student.id)
            if not result:
                print("No match found.")

    # Teacher Functions

    def add_teacher(self, name, specialty):
        """Adds a teacher to the system."""
        new_teacher = TeacherUser(
            name = name,
            teacher_id = self.next_teacher_id,
            specialty = specialty
        )
        self.teachers.append(new_teacher)
        self.next_teacher_id += 1
        self._save_data()
        return True

    def remove_teacher(self, teacher_id):
        """Removes an existing teacher from the system."""
        teacher = self.find_by_id(teacher_id, search="teacher")
        if teacher:
            self.teachers.remove(teacher)
            print(f"Teacher ID {teacher_id} has been removed.")
            self._save_data()
            return True
        else:
            print(f"Teacher ID {teacher_id} not found.")
            return False

    def find_teachers(self, term):
        """Finds teachers by name, specialty or id."""
        try:
            term = int(term)
            id_search = True
        except ValueError:
            id_search = False
        print(f"\n--- Finding teacher matching '{term}' ---")
        # Searches teacher database for student with the id provided.
        if id_search:
            if self.find_by_id(term, search="teacher"):
                self.get_teacher_details(term)
            else:
                print(f"Teacher ID {term} not found.")
        else:
            # Filters the teacher database for teachers with names or specialties matching the search term.
            result = [teacher for teacher in self.teachers if
                      term.lower() in teacher.name.lower() or term.lower() in teacher.specialty.lower()]
            for teacher in result:
                self.get_teacher_details(teacher.id)
            if not result:
                print("No match found.")

    def get_teacher_details(self, teacher_id):
        """Prints a teacher's details."""
        teacher = self.find_by_id(teacher_id, search="teacher")
        if teacher:
            print(teacher)
            print("-" * 20)
        else:
            print(f"Error: Teacher ID {teacher_id} not found.")

    def list_teachers(self):
        """Prints all teachers in the application data."""
        if self.teachers:
            print("\n--- Teacher List ---")
            for teacher in self.teachers:
                self.get_teacher_details(teacher.id)
        else:
            print("Error: No teachers found in the system.")

    # Course Functions

    def add_course(self, name, instrument, teacher_id):
        """Adds a course to the system."""
        teacher = self.find_by_id(teacher_id, search="teacher")
        if teacher:
            new_course = Course(
                name=name,
                course_id=self.next_course_id,
                instrument=instrument,
                teacher_id=teacher_id,
            )
            self.courses.append(new_course)
            print(f"Course ID {self.next_course_id} added.")
            self.next_course_id += 1
            self._save_data()
            return True
        else:
            print(f"Teacher ID {teacher_id} not found.")
            return False

    def remove_course(self, course_id):
        """Removes an existing teacher from the system."""
        course = self.find_by_id(course_id, search="course")
        if course:
            self.courses.remove(course)
            print(f"Course ID {course_id} has been removed.")
            self._save_data()
            return True
        else:
            print(f"Course ID {course_id} not found.")
            return False

    def add_lesson(self, course_id, lesson_day, start_time, room):
        """Adds a new lesson to a course in the system."""
        course = self.find_by_id(course_id, search="course")
        day_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        try:
            day = parser.parse(lesson_day, fuzzy=True).strftime("%A")
        except ValueError:
            best_match = difflib.get_close_matches(lesson_day, day_list, n=1, cutoff=0.6)
            if best_match:
                day = best_match[0]
            else:
                print("Error: Lesson day invalid.")
                return False

        if isinstance(start_time, dt.time):
            start_time = start_time.strftime("%H:%M")
        if course:
            new_lesson = {
                "lesson_id": self.next_lesson_id,
                "day": day,
                "start_time": start_time,
                "room": room,
            }
            self.next_lesson_id += 1
            course.lessons.append(new_lesson)
            self._save_data()
            print("Lesson added to course.")
            return True
        else:
            print(f"Course ID {course_id} not found.")
            return False

    def find_courses(self, term):
        """Finds courses by name, specialty or id."""
        try:
            term = int(term)
            id_search = True
        except ValueError:
            id_search = False
        print(f"\n--- Finding course matching '{term}' ---")
        # Searches system for course with the id provided.
        if id_search:
            if self.find_by_id(term, search="course"):
                self.get_course_details(term)
            else:
                print(f"Teacher ID {term} not found.")
        else:
            # Filters the system for courses with names matching the term.
            result = [course for course in self.courses if term.lower() in course.name.lower()]
            for course in result:
                self.get_course_details(course.id)
            if not result:
                print("No match found.")

    def get_course_details(self, course_id):
        """Prints a course's details."""
        course = self.find_by_id(course_id, search="course")
        if course:
            print(course)
            print("-" * 20)
        else:
            print(f"Error: Course ID {course_id} not found.")

    def list_courses(self):
        """Prints all courses in the system."""
        if self.courses:
            print("\n--- Course List ---")
            for course in self.courses:
                self.get_course_details(course.id)
        else:
            print("Error: No teachers found in the system.")

    def get_lessons(self, course_id):
        """Gets the lessons for a course"""
        course = self.find_by_id(course_id, search="course")
        if course:
            course.get_lessons()
        else:
            print(f"Error: Course ID {course_id} not found.")

    def daily_roster(self, day):
        """Displays a pretty table of all lessons on a given day."""
        lessons = []
        for course in self.courses:
            for lesson in course.lessons:
                if lesson["day"] == day:
                    teacher = self.find_by_id(course.teacher_id, search="teacher")
                    sel_lesson = {
                        "Course" : course.name,
                        "Lesson id": lesson["lesson_id"],
                        "Teacher" : teacher.name,
                        "Time" : lesson["start_time"],
                        "Room" : lesson["room"],
                    }
                    lessons.append(sel_lesson)
        if lessons:
            return lessons
        return None

    # Finance functions

    def record_payment(self, student_id, amount, method):
        """Adds a payment record to the finance log."""
        student = self.find_by_id(student_id, search="student")
        if student:
            # Create a payment dictionary with student_id, amount, method, and a timestamp.
            payment_record = {
                "student_id": student_id,
                "amount": amount,
                "method": method,
                "timestamp": dt.datetime.now().isoformat()
            }
            # TODO: Append the record to self.finance_log and save the data.
            self.finance_log.append(payment_record)
            self._save_data()
            print(f"Payment of {amount} for student {student_id} recorded.")
            return True
        else:
            print("Student not found.")
            return False

    def get_payment_history(self, student_id):
        """Returns a list of all payments for a given student."""
        return [p for p in self.finance_log if p['student_id'] == student_id]

    def export_report(self, kind, out_path="PST5/assets"):
        """Exports a log to a CSV file."""
        print(f"Exporting {kind} report to {out_path}...")
        if kind == "finance":
            data_to_export = self.finance_log
            headers = ["student_id", "amount", "method", "timestamp"]
        elif kind == "attendance":
            data_to_export = self.attendance_log
            headers = ["student_id", "course_id", "timestamp"]
        else:
            print("Error: Unknown report type.")
            return False
        with open(f"{out_path}/{kind}_report.csv", "w") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data_to_export)
            print("Report generated.")
            return True



    # Object data helper functions

    def update_information(self, id_, type_ = "student", **kwargs):
        """Updates the information of the selected type."""
        name = kwargs.get("name")
        specialty = kwargs.get("specialty")
        instrument = kwargs.get("instrument")
        teacher_id = kwargs.get("teacher_id")
        if type_ == "student":
            student = self.find_by_id(id_)
            if name:
                student.name = name
        elif type_ == "teacher":
            teacher = self.find_by_id(id_, search="teacher")
            if name:
                teacher.name = name
            if specialty:
                teacher.specialty = specialty
        elif type_ == "course":
            course = self.find_by_id(id_, search="course")
            if name:
                course.name = name
            if instrument:
                course.instrument = instrument
            if teacher_id:
                course.teacher_id = teacher_id
        self._save_data()
        return True

    def school_lookup(self, term, search=None):
        """High-level function to search everything."""
        print(f"\n--- Performing lookup for '{term}' ---")
        if search.lower() == "student":
            self.find_students(term)
        elif search.lower() == "teacher":
            self.find_teachers(term)
        elif search.lower() == "course":
            self.find_courses(term)
        else:
            print("Error: Search type invalid.")

    def find_by_id(self, id_, search="student"):
        """Finds a student, teacher or course with the provided id. Default is student search.
        Returns None if no matching object is found."""
        if search == "student":
            for student in self.students:
                if student.id == id_:
                    return student
        elif search == "teacher":
            for teacher in self.teachers:
                if teacher.id == id_:
                    return teacher
        elif search == "course":
            for course in self.courses:
                if course.id == id_:
                    return course
        else:
            raise "Error: Search type invalid"
        return None

    # High level functions

    def register_student(self, name, course_id):
        """High-level function to register a new student and enrol them."""
        student = self.add_student(name)
        # Enrols new student in provided instrument
        enrol = self.enrol_student(student, course_id)
        if not enrol:
            self.remove_student(student)
            return False
        else:
            print(f"Student registered.")
            return True

    def switch_course(self, student_id, from_course_id, to_course_id):
        """Switches a students course from one to another"""
        # Checks if both course ids provided are the same.
        if from_course_id == to_course_id:
            return False

        old_course = self.disenroll_student(student_id, from_course_id)

        # Makes sure the student disenrolled is successful before continuing.
        if not old_course:
            return False
        new_course = self.enrol_student(student_id, to_course_id)
        if new_course:
            return True

        # Returns student enrollment status to original if student enrollment is unsuccessful.
        self.enrol_student(student_id, from_course_id)
        return False

    # Data conversion functions

    def student_to_df(self):
        """Converts student data to a dataframe"""
        with open(file=self.file_path, mode="r") as file:
            data = json.load(file)["students"]
            for student in data:
                courses = []
                for course in student["enrolled_courses"]:
                    sel_course = self.find_by_id(course, search="course")
                    courses.append(sel_course.name)
                student["enrolled_courses"] = courses
            df = pd.DataFrame(data)
            return df

    def teacher_to_df(self):
        """Converts teacher data to a dataframe"""
        with open(file=self.file_path, mode="r") as file:
            data = json.load(file)["teachers"]
            df = pd.DataFrame(data)
            return df

    def course_to_df(self):
        """Converts course data to a dataframe"""
        with open(file=self.file_path, mode="r") as file:
            data = json.load(file)["courses"]
            for course in data:
                course.pop("lessons", None)
            df = pd.DataFrame(data)
            return df

