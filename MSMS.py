# Data Models
class Student:
    """A blueprint for student objects. Stores student info as attributes."""
    def __init__(self, name, student_id):
        self.name = name
        self.id = student_id
        self.enrolled_in = []
    
    def get_details(self):
        """Prints a formatted string containing the students details."""
        print(f"ID: {self.id}\nName: {self.name.title()}\nEnrolled in: {self.enrolled_in}")

class Teacher:
    """A blueprint for teacher objects. Stores teacher info as attributes."""
    def __init__(self, name, teacher_id, specialty):
        self.name = name
        self.id = teacher_id
        self.specialty = specialty
    
    def get_details(self):
        """Prints a formatted string containing the teachers details."""
        print(f"ID: {self.id}\nName: {self.name.title()}\nSpecialty: {self.specialty.title()}")


# In-Memory Databases
student_db = []
teacher_db = []
student_id_next = 1
teacher_id_next = 1 

# Core Helper Functions

def add_teacher(name, specialty):
    """Create a Teacher object and adds it to the database."""
    global teacher_id_next
    new_teacher = Teacher(
        name=name,
        teacher_id=teacher_id_next,
        specialty=specialty,
    )
    teacher_db.append(new_teacher)
    teacher_id_next += 1

def list_students():
    """Prints all students in the database."""
    if student_db:
        print("\n--- Student List ---")
        for student in student_db:
            student.get_details()
            print("-" * 15)    
    else:
        print("No students found in the system.")

def list_teachers():
    """Prints all teachers in the database."""
    if teacher_db:
        print("\n--- Teacher List ---")
        for teacher in teacher_db:
            teacher.get_details()
            print("-" * 15)
    else:
        print("No teachers found in the system.")

def find_students(term: str):
    """Finds students by name."""
    print(f"\n--- Finding students matching '{term}' ---")
    # Filters the student database for students with names matching the search term.
    result = [student for student in student_db if term.lower() in student.name.lower()]
    for student in result:
        student.get_details()
        print("-" * 15)
    if not result:
        print("No match found.")

def find_teachers(term: str):
    """Finds teachers by name or specialty."""
    print(f"\n--- Finding teachers matching '{term}' ---")
    # Filters the student database for teachers with names or specialties matching the search term.
    result = [teacher for teacher in teacher_db if term.lower() in teacher.name.lower() or term.lower() in teacher.specialty.lower()]
    for teacher in result:
        teacher.get_details()
        print("-" * 15)
    if not result:
        print("No match found.")

# Front Desk Functions
def find_student_by_id(student_id):
    """Finds a student with the provided student id."""
    for student in student_db:
        if student.id == student_id:
            return student
    return None
        
def front_desk_register(name, instrument):
    """High-level function to register a new student and enrol them."""
    global student_id_next
    new_student = Student(
        name=name,
        student_id=student_id_next,
    )
    student_db.append(new_student)
    student_id_next += 1

    # Enrols new student in provided instrument
    front_desk_enrol(new_student.id, instrument=instrument)
    print(f"Front Desk: Successfully registered '{name}' and enrolled them in '{instrument}'.")


def front_desk_enrol(student_id, instrument):
    """High-level function to enrol an existing student in a course."""
    enrolling_student = find_student_by_id(student_id)
    if enrolling_student:
        # Checks if student is already enrolled in an instrument.
        for enrolled_instrument in enrolling_student.enrolled_in:
            if instrument.lower() in enrolled_instrument.lower():
                print(f"Error: Student ID {student_id} already enrolled in {instrument}.")
                break
        # Runs if student is not already enrolled in the instrument.
        else:
            enrolling_student.enrolled_in.append(instrument.title())
            print(f"Front Desk: Enrolled student ID {student_id} in '{instrument}'.")
    else:
        print(f"Error: Student ID {student_id} not found.")

def front_desk_unenrol(student_id):
    """High-level function to unenrol an existing student in a course."""
    selected_student = find_student_by_id(student_id)
    if selected_student:
        enrolled_instruments = selected_student.enrolled_in
        if enrolled_instruments:
            # Lists instruments the current student is enrolled in and waits for user input.
            print(f"The current student is enrolled in {enrolled_instruments}")
            instrument = input("Please select which instrument to unenrol the student in.\n")
            # Checks if student is enrolled in the instrument.
            try: 
                enrolled_instruments.remove(instrument)
                print(f"Front Desk: Unenrolled student {student_id} in {instrument}.")
            except ValueError:
                print(f"Error: The current student is not enrolled in {instrument}.")
        else:
            print("The current student is not enrolled in any instruments.")
    else:
        print(f"Error: Student ID {student_id} not found.")

def front_desk_lookup(term: str):
    """High-level function to search everything."""
    print(f"\n--- Performing lookup for '{term}' ---")
    find_students(term)
    find_teachers(term)


# Main Application
def main():
    """Runs the main interactive menu for the receptionist."""
    

    while True:
        print("\n===== Music School Front Desk =====")
        print("1. Register New Student")
        print("2. Enrol Existing Student")
        print("3. Unenroll Existing Student")
        print("4. Lookup Student or Teacher")
        print("5. (Admin) Register New Teacher")
        print("6. (Admin) List all Students")
        print("7. (Admin) List all Teachers")
        print("q. Quit")

        choice = input("Enter your choice: ")
        
        if choice == "1":
            # Registers New Student
            student_name = input("Enter student name: ")
            instrument = input("Enter instrument to enrol in: ")
            front_desk_register(student_name, instrument=instrument)

        elif choice == "2":
            # Enrols Existing Student
            try:
                student_id = int(input("Enter student ID: "))
                instrument = input("Enter instrument to enrol in: ")
                front_desk_enrol(student_id, instrument)
            except ValueError:
                print("Invalid ID. Please enter a number.")

        elif choice == "3":
            # Unenrols Existing Student
            try:
                student_id = int(input("Enter student ID: "))
                front_desk_unenrol(student_id)
            except ValueError:
                print("Invalid ID. Please enter a number.")

        elif choice == "4":
            # Searches students and teachers
            term = input("Enter search term:")
            front_desk_lookup(term)

        elif choice == "5":
            # Adds new teacher
            teacher_name = input("Enter teacher name: ")
            specialty = input("Enter teacher specialty: ")
            add_teacher(teacher_name, specialty=specialty)

        elif choice == "6":
            # Lists all students
            list_students()

        elif choice == "7":
            # Lists all teachers
            list_teachers()

        elif choice.lower() == "q":
            # Quits program
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

# Program Start
if __name__ == "__main__":
    main()