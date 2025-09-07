from user import User

class StudentUser(User):
    """Represents a student user, inheriting from the base User class."""
    def __init__(self, student_id, name):
        super().__init__(student_id, name)
        self.enrolled_courses = []