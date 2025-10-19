from app.student import StudentUser
from app.teacher import  TeacherUser, Course
import json
import datetime as dt
from dateutil import parser
import difflib


class ScheduleManager:

    def __init__(self, file_path="PST3/data/msms.json"):
        self.students = []
        self.teachers = []
        self.courses = []
        self.attendance_log = []
        self.next_student_id = 1
        self.next_teacher_id = 1
        self.next_course_id = 101
        self.next_lesson_id = 1
        self.file_path = file_path
        self._load_data()
        print(self.courses)

    # Data management functions.
    def _load_data(self):
        try:
            with open(file=self.file_path, mode="r") as file:
                data = json.load(file)

                # Initializes all data from the json
                self.load_students(data["students"])
                self.load_teachers(data["teachers"])
                self.load_courses(data["courses"])
                for record in data.get("attendance", []):
                    self.attendance_log.append(record)

                # Checks if the current data file contains id counters.
                # If not, sets them to the next number from the highest id.
                # If there is no data for the counters, sets it to the default value.
                self.next_student_id = max(student.id for student in self.students) + 1 if self.students else 1
                self.next_teacher_id = max(teacher.id for teacher in self.teachers) + 1 if self.teachers else 1
                self.next_course_id = max(course.id for course in self.courses) + 1 if self.courses else 101            # Counter for lessons
                lesson_list = [course.lessons for course in self.courses]
                all_lessons = []
                # Flatten lesson_list
                for element in lesson_list:
                    if type(element) == list:
                        for lesson in element:
                            all_lessons.append(lesson)
                    else:
                        all_lessons.append(element)
                self.next_lesson_id = data.get("next_lesson_id") or (max(lesson["lesson_id"] for lesson in all_lessons) + 1) if all_lessons else 1
        except FileNotFoundError:
            pass
    


    def _save_data(self):
        app_data = {
            "students": [student.__dict__ for student in self.students],
            "teachers": [teacher.__dict__ for teacher in self.teachers],
            "courses": [course.__dict__ for course in self.courses],
            "attendance": self.attendance_log,
        }
        with open(file=self.file_path, mode="w") as file:
            json.dump(app_data, fp=file, indent=5)

    # Data management helper functions.
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
        self.next_student_id += 1
        self._save_data()
        return new_student.id

    def remove_student(self, student_id):
        student = self.find_by_id(student_id)
        print(student)
        if student:
            self.students.remove(student)
            print(f"Successfully removed student ID {student_id}.")
            self._save_data()
        else:
            print(f"Error: Student ID {student_id} not found.")

    def enrol_student(self, student_id, course_id):
        student = self.find_by_id(student_id)
        course = self.find_by_id(course_id, search="course")
        if not (student and course):
            print("Error: Student ID or Course ID invalid.")
            return False
        if course_id in student.enrolled_courses or student_id in course.enrolled_students:
            print("Error: Student already enrolled in course.")
            return False
        student.enrolled_courses.append(course_id)
        course.enrolled_students.append(student_id)
        print(f"Enrolled student ID {student_id} in course ID {course_id}")
        self._save_data()
        return True

    def disenroll_student(self, student_id, course_id):
        student = self.find_by_id(student_id)
        course = self.find_by_id(course_id, search="course")
        if not (student and course):
            print("Error: Student ID or Course ID invalid.")
            return False
        if course_id in student.enrolled_courses or student_id in course.enrolled_students:
            student.enrolled_courses.remove(course_id)
            course.enrolled_students.remove(student_id)
            print(f"Disenrolled student ID {student_id} in course ID {course_id}")
            self._save_data()
            return True
        print("Error: Student not enrolled in course.")
        return False

    def check_in(self, student_id, course_id, timestamp):
        """Records a student's attendance for a course."""
        if not timestamp:
            timestamp = dt.datetime.now().isoformat()
        else:
            try:
                timestamp = parser.parse(timestamp).isoformat()
            except ValueError:
                print("An error occurred, using current date and time.")
                timestamp = dt.datetime.now().isoformat()

        student = self.find_by_id(student_id)
        course = self.find_by_id(course_id, search="course")

        if not student or not course:
            print("Error: Check-in failed. Invalid Student or Course ID.")
            return False

        if course.id in student.enrolled_courses:
            new_record = {
                "student_id": student.id,
                "course_id": course.id,
                "timestamp": timestamp
            }
            self.attendance_log.append(new_record)
            self._save_data()
            print(f"Success: Student {student.name} checked into {course.name}")
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
            print(f"Error: Student ID {student_id} not found.")

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

    def remove_teacher(self, teacher_id):
        """Removes an existing teacher from the system."""
        teacher = self.find_by_id(teacher_id, search="teacher")
        if teacher:
            self.teachers.remove(teacher)
            print(f"Teacher ID {teacher_id} has been removed.")
            self._save_data()
        else:
            print(f"Error: Teacher ID {teacher_id} not found.")


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
            self.next_course_id += 1
            self._save_data()
        else:
            print(f"Error: Teacher ID {teacher_id} not found.")

    def remove_course(self, course_id):
        """Removes an existing teacher from the system."""
        course = self.find_by_id(course_id, search="course")
        if course:
            self.courses.remove(course)
            print(f"Course ID {course_id} has been removed.")
            self._save_data()
        else:
            print(f"Error: Course ID {course_id} not found.")

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
                return
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
        else:
            print(f"Error: Course ID {course_id} not found.")

    # Object data helper functions
    def update_information(self, id_, type_ = "student", **kwargs):
        name = kwargs.get("name")
        specialty = kwargs.get("specialty")
        instrument = kwargs.get("instrument")
        if type_ == "student":
            student = self.find_by_id(id_)
            if name:
                student.name = name
            print(f"Successfully changed student ID {id_} data.")
        elif type_ == "teacher":
            teacher = self.find_by_id(id_, search="teacher")
            if name:
                teacher.name = name
            if specialty:
                teacher.specialty = specialty
            print(f"Successfully changed teacher ID {id_} data.")
        elif type_ == "course":
            course = self.find_by_id(id_, search="course")
            if name:
                course.name = name
            if instrument:
                course.instrument = instrument
            print(f"Successfully changed course ID {id_} data.")
        self._save_data()

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

