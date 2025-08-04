# Data Models
class Student:
    """A blueprint for student objects. Stores student info as attributes."""
    def __init__(self, name, student_id):
        self.name = name
        self.id = student_id
        self.enrolled_in = []

class Teacher:
    """A blueprint for teacher objects. Stores teacher info as attributes."""
    def __init__(self, name, teacher_id, specialty):
        self.name = name
        self.id = teacher_id
        self.specialty = specialty


# In-Memory Databases
student_db = []
teacher_db = []
student_id_next = 1
teacher_id_next = 1 