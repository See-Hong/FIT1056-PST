from user import User

class TeacherUser(User):
    """Represents a teacher user, inheriting from the base User class."""
    def __init__(self, teacher_id, name, specialty):
        super().__init__(teacher_id, name)
        self.specialty = specialty

class Course:
    """Base class for courses in the system."""
    def __init__(self, course_id, name, instrument, teacher_id):
        self.id = course_id
        self.name = name
        self.instrument = instrument
        self.teacher_id = teacher_id
        self.enrolled_students = []
        self.lessons = []

