from student import StudentUser
from teacher import  TeacherUser, Course
import json


class ScheduleManager:

    def __init__(self, file_path):
        self.students = []
        self.teachers = []
        self.courses = []
        self.attendance_log = []
        self.file_path = file_path
        self._load_data()

    def _load_data(self):
        with open(file=self.file_path, mode="r") as file:
            data = json.load(file)

            # Initializes all data from the json
            self.load_students(data["students"])
            self.load_teachers(data["teachers"])
            self.load_courses(data["courses"])
            self.load_attendance(data.get("attendance"))


    def _save_data(self):
        app_data = {
            "students": [student.__dict__ for student in self.students],
            "teachers": [teacher.__dict__ for teacher in self.teachers],
            "courses": [course.__dict__ for course in self.courses],
            "attendance": self.attendance_log,
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

    def load_attendance(self, data):
        """Initializes attendance data with the given data."""
        for record in data:
            self.attendance_log.append(record)
