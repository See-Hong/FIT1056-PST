from app5.user import User

class TeacherUser(User):
    """Represents a teacher user, inheriting from the base User class."""
    def __init__(self, teacher_id, name, specialty):
        super().__init__(teacher_id, name)
        self.specialty = specialty

    def __str__(self):
        """String representation of a teacher object."""
        return (f"Name: {self.name}"
                f"\nID: {self.id}"
                f"\nSpecialty: {self.specialty}")

class Course:
    """Base class for courses in the system."""
    def __init__(self, course_id, name, instrument, teacher_id):
        self.id = course_id
        self.name = name
        self.instrument = instrument
        self.teacher_id = teacher_id
        self.enrolled_students = []
        self.lessons = []

    def __str__(self):
        """String representation of a course object"""
        return (f"Name: {self.name}"
                f"\nCourse ID: {self.id}"
                f"\nInstrument: {self.instrument}"
                f"\nTeacher ID: {self.teacher_id}"
                f"\nEnrolled Student ID: {self.enrolled_students}"
                )

    def get_lessons(self):
        """Gets the lessons for a course."""
        for lesson in self.lessons:
            print(f"Name: {self.name}"
                  f"\nLesson ID: {lesson["lesson_id"]}"
                  f"\nDay: {lesson["day"]}"
                  f"\nStart Time: {lesson["start_time"]}"
                  f"\nRoom: {lesson["room"]}")
            print("-" * 20)

