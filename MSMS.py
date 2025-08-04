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

# Core Helper Functions

def add_teacher(name, speciality):
    """Create a Teacher object and adds it to the database."""
    global teacher_id_next
    new_teacher = Teacher(
        name=name,
        teacher_id=teacher_id_next,
        specialty=speciality
    )
    teacher_db.append(new_teacher)
    teacher_id_next += 1

def list_students():
    """Prints all students in the database."""
    if student_db:
        print("\n--- Student List ---")
        for student in student_db:
            print(f"ID: {student.id}\nName: {student.name}\nEnrolled in: {student.enrolled_in}")
            print("-" * 15)    
    else:
        print("No students found in the system.")

def list_teachers():
    """Prints all teachers in the database."""
    if teacher_db:
        print("\n--- Teacher List ---")
        for teacher in teacher_db:
            print(f"ID: {teacher.id}\nName: {teacher.name}\nSpecialty: {teacher.specialty}")
            print("-" * 15)
    else:
        print("No teachers found in the system.")

def find_students(term: str):
    """Finds students by name."""
    print(f"\n--- Finding students matching '{term}' ---")
    # Filters the student database for students with names matching the search term.
    result = [student for student in student_db if term.lower() in student.name.lower()]
    for student in result:
        print(f"ID: {student.id}\nName: {student.name}\nEnrolled in: {student.enrolled_in}")
        print("-" * 15)
    if not result:
        print("No match found.")

def find_teachers(term: str):
    """Finds teachers by name or specialty."""
    print(f"\n--- Finding teachers matching '{term}' ---")
    # Filters the student database for teachers with names or specialties matching the search term.
    result = [teacher for teacher in teacher_db if term.lower() in teacher.name.lower() or term.lower() in teacher.specialty.lower()]
    for teacher in result:
        print(f"ID: {teacher.id}\nName: {teacher.name}\nSpecialty: {teacher.specialty}")
        print("-" * 15)
    if not result:
        print("No match found.")

