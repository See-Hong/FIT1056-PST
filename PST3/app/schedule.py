from student import StudentUser
from teacher import  TeacherUser, Course
import json
import datetime as dt
from dateutil import parser


class ScheduleManager:

    def __init__(self, file_path):
        self.students = []
        self.teachers = []
        self.courses = []
        self.attendance_log = []
        self.next_student_id = 1
        self.next_teacher_id = 1
        self.next_course_id = 101
        self.file_path = file_path
        self._load_data()

    def _load_data(self):
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
            self.next_student_id = data.get("next_student_id") or (max(student.id for student in self.students) + 1 if self.students else 1)
            self.next_teacher_id = data.get("next_teacher_id") or (max(teacher.id for teacher in self.teachers) + 1 if self.teachers else 1)
            self.next_course_id = data.get("next_course_id") or (max(course.id for course in self.courses) + 1 if self.courses else 101)


    def _save_data(self):
        app_data = {
            "students": [student.__dict__ for student in self.students],
            "teachers": [teacher.__dict__ for teacher in self.teachers],
            "courses": [course.__dict__ for course in self.courses],
            "attendance": self.attendance_log,
            "next_student_id": self.next_student_id,
            "next_teacher_id": self.next_teacher_id,
            "next_course_id": self.next_course_id,
        }
        with open(file=self.file_path, mode="w") as file:
            json.dump(app_data, fp=file, indent=5)

    def load_students(self, data):
        """Initializes student objects with the given data."""
        for student in data:
            new_student = StudentUser(
                student_id=student["id"],
                name=student["name"]
            )
            new_student.enrolled_courses = student.get("enrolled_course_ids", [])
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
            new_course.enrolled_students = course.get("enrolled_student_ids", [])
            new_course.lessons = course.get("lessons", [])
            self.courses.append(new_course)

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

