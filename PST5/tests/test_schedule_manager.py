# tests/test_schedule_manager.py
import pytest
import os
import sys
import datetime as dt

current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, project_root)

from app.schedule import ScheduleManager

@pytest.fixture
def fresh_manager():
    """Creates a fresh ScheduleManager instance using a temporary test data file."""
    test_file = "test_data.json"
    if os.path.exists(test_file):
        os.remove(test_file)
    return ScheduleManager(file_path=test_file)

def test_add_student(fresh_manager):
    name = "Bob"
    student_id = fresh_manager.add_student(name)

    assert len(fresh_manager.students) == 1
    assert fresh_manager.students[0].name == name
    assert fresh_manager.students[0].id == student_id
    assert len(fresh_manager.students[0].enrolled_courses) == 0

@pytest.mark.parametrize("invalid_name", ["", "     ", "123", "@lice!", "Bob#1"])
def test_add_student_invalid_names(fresh_manager, invalid_name):
    result = fresh_manager.add_student(invalid_name)

    assert result == False
    assert len(fresh_manager.students) == 0

def test_add_student_duplicate(fresh_manager):
    id_1 = fresh_manager.add_student("Adam")
    id_2 = fresh_manager.add_student("Adam")

    assert len(fresh_manager.students) == 2
    assert fresh_manager.students[0].name == fresh_manager.students[1].name
    assert id_1 != id_2

def test_add_teacher(fresh_manager):
    name = "Jack"
    specialty = "Piano"
    teacher_id = fresh_manager.add_teacher(name, specialty)

    assert len(fresh_manager.teachers) == 1
    assert fresh_manager.teachers[0].name == name
    assert fresh_manager.teachers[0].specialty == specialty
    assert fresh_manager.teachers[0].id == teacher_id

@pytest.mark.parametrize("invalid_name, specialty", [("", "Guitar"), ("     ", "Piano"), ("123", "Violin"), ("@lice!", "Bass"), ("Bob#1", "Piano")])
def test_add_teacher_invalid_names(fresh_manager, invalid_name, specialty):
    result = fresh_manager.add_teacher(invalid_name, specialty)

    assert result == False
    assert len(fresh_manager.teachers) == 0

@pytest.mark.parametrize("name, invalid_specialty", [("Bob", ""), ("Tom","     "), ("Alice", "123")])
def test_add_teacher_invalid_specialty(fresh_manager, name, invalid_specialty):
    result = fresh_manager.add_teacher(name, invalid_specialty)

    assert result == False
    assert len(fresh_manager.teachers) == 0

def test_add_teacher_duplicate(fresh_manager):
    id_1 = fresh_manager.add_teacher("James", "Piano")
    id_2 = fresh_manager.add_teacher("James", "Piano")

    assert len(fresh_manager.teachers) == 2
    assert fresh_manager.teachers[0].name == fresh_manager.teachers[1].name
    assert fresh_manager.teachers[0].specialty == fresh_manager.teachers[1].specialty
    assert id_1 != id_2

def test_add_course(fresh_manager):
    teacher_id = fresh_manager.add_teacher("Bob", "Piano")
    name = "Beginner Piano"
    specialty = "Piano"
    course_id = fresh_manager.add_course(name, specialty, teacher_id)

    assert len(fresh_manager.courses) == 1
    assert fresh_manager.courses[0].id == course_id
    assert fresh_manager.courses[0].name == name
    assert fresh_manager.courses[0].instrument == specialty
    assert fresh_manager.courses[0].teacher_id == teacher_id
    assert len(fresh_manager.courses[0].enrolled_students) == 0
    assert len(fresh_manager.courses[0].lessons) == 0

def test_add_course_no_teacher(fresh_manager):
    result = fresh_manager.add_course("Beginner Guitar", "Guitar", teacher_id=1)

    assert result == False
    assert len(fresh_manager.courses) == 0

@pytest.mark.parametrize("invalid_name, instrument", [("", "Guitar"), ("     ", "Piano"), ("123", "Violin")])
def test_add_course_invalid_names(fresh_manager, invalid_name, instrument):
    teacher_id = fresh_manager.add_teacher("Bob", "Piano")
    result = fresh_manager.add_course(invalid_name, instrument, teacher_id)

    assert result == False
    assert len(fresh_manager.courses) == 0

@pytest.mark.parametrize("name, invalid_instrument", [("Guitar", ""), ("Piano", "     "), ("Violin","123")])
def test_add_course_invalid_instruments(fresh_manager, name, invalid_instrument):
    teacher_id = fresh_manager.add_teacher("Bob", "Piano")
    result = fresh_manager.add_course(name, invalid_instrument, teacher_id)

    assert result == False
    assert len(fresh_manager.courses) == 0

def test_add_course_duplicate(fresh_manager):
    teacher_id = fresh_manager.add_teacher("Bob", "Piano")
    id_1 = fresh_manager.add_course("Beginner Piano", "Piano", teacher_id)
    id_2 = fresh_manager.add_course("Beginner Piano", "Piano", teacher_id)

    assert len(fresh_manager.courses) == 2
    assert fresh_manager.courses[0].name == fresh_manager.courses[1].name
    assert fresh_manager.courses[0].instrument == fresh_manager.courses[1].instrument
    assert fresh_manager.courses[0].teacher_id == fresh_manager.courses[1].teacher_id
    assert id_1 != id_2

def test_enrol_student(fresh_manager):
    student_id = fresh_manager.add_student("Bob")
    teacher_id = fresh_manager.add_teacher("James", "Guitar")
    course_id = fresh_manager.add_course("Guitar", "Guitar", teacher_id)
    fresh_manager.enrol_student(student_id, course_id)

    assert fresh_manager.students[0].enrolled_courses[0] == course_id
    assert fresh_manager.courses[0].enrolled_students[0] == student_id

def test_enrol_student_already_enrolled(fresh_manager):
    student_id = fresh_manager.add_student("Bob")
    teacher_id = fresh_manager.add_teacher("James", "Guitar")
    course_id = fresh_manager.add_course("Guitar", "Guitar", teacher_id)
    fresh_manager.enrol_student(student_id, course_id)
    enrol = fresh_manager.enrol_student(student_id, course_id)

    assert enrol == False
    assert fresh_manager.students[0].enrolled_courses[0] == course_id
    assert fresh_manager.courses[0].enrolled_students[0] == student_id

def test_enrol_student_invalid_student(fresh_manager):
    teacher_id = fresh_manager.add_teacher("James", "Guitar")
    course_id = fresh_manager.add_course("Guitar", "Guitar", teacher_id)
    enrol = fresh_manager.enrol_student(12, course_id)

    assert enrol == False
    assert len(fresh_manager.courses[0].enrolled_students) == 0

def test_enrol_student_invalid_course(fresh_manager):
    student_id = fresh_manager.add_student("Bob")
    enrol = fresh_manager.enrol_student(student_id, 11)

    assert enrol == False
    assert len(fresh_manager.students[0].enrolled_courses) == 0

def test_disenroll_student(fresh_manager):
    student_id = fresh_manager.add_student("Bob")
    teacher_id = fresh_manager.add_teacher("James", "Guitar")
    course_id = fresh_manager.add_course("Guitar", "Guitar", teacher_id)
    fresh_manager.enrol_student(student_id, course_id)
    fresh_manager.disenroll_student(student_id, course_id)

    assert len(fresh_manager.students[0].enrolled_courses) == 0
    assert len(fresh_manager.courses[0].enrolled_students) == 0

def test_disenroll_student_not_enrolled(fresh_manager):
    student_id = fresh_manager.add_student("Bob")
    teacher_id = fresh_manager.add_teacher("James", "Guitar")
    course_id = fresh_manager.add_course("Guitar", "Guitar", teacher_id)
    disenroll = fresh_manager.disenroll_student(student_id, course_id)

    assert disenroll == False

def test_disenroll_student_invalid_student(fresh_manager):
    student_id = fresh_manager.add_student("Bob")
    teacher_id = fresh_manager.add_teacher("James", "Guitar")
    course_id = fresh_manager.add_course("Guitar", "Guitar", teacher_id)
    fresh_manager.enrol_student(student_id, course_id)
    disenroll = fresh_manager.disenroll_student(123, course_id)

    assert disenroll == False

def test_disenroll_student_invalid_course(fresh_manager):
    student_id = fresh_manager.add_student("Bob")
    teacher_id = fresh_manager.add_teacher("James", "Guitar")
    course_id = fresh_manager.add_course("Guitar", "Guitar", teacher_id)
    fresh_manager.enrol_student(student_id, course_id)
    disenroll = fresh_manager.disenroll_student(student_id, 123)

    assert disenroll == False

def test_remove_student(fresh_manager):
    student_id = fresh_manager.add_student("Bob")
    teacher_id = fresh_manager.add_teacher("James", "Guitar")
    course_id = fresh_manager.add_course("Guitar", "Guitar", teacher_id)
    fresh_manager.enrol_student(student_id, course_id)
    fresh_manager.remove_student(student_id)

    assert len(fresh_manager.students) == 0
    assert len(fresh_manager.courses[0].enrolled_students) == 0

def test_remove_student_invalid_student(fresh_manager):
    remove = fresh_manager.remove_student(123)

    assert remove == False

def test_remove_student_multiple_enrollment(fresh_manager):
    student_id = fresh_manager.add_student("Bob")
    teacher_id = fresh_manager.add_teacher("James", "Guitar")
    course_id_1 = fresh_manager.add_course("Guitar", "Guitar", teacher_id)
    course_id_2 = fresh_manager.add_course("Piano", "Piano", teacher_id)
    fresh_manager.enrol_student(student_id, course_id_1)
    fresh_manager.enrol_student(student_id, course_id_2)
    fresh_manager.remove_student(student_id)

    assert len(fresh_manager.courses[0].enrolled_students) == 0
    assert len(fresh_manager.courses[1].enrolled_students) == 0

def test_check_in(fresh_manager):
    student_id = fresh_manager.add_student("Bob")
    teacher_id = fresh_manager.add_teacher("James", "Guitar")
    course_id = fresh_manager.add_course("Guitar", "Guitar", teacher_id)
    fresh_manager.enrol_student(student_id, course_id)
    today = dt.datetime.now()
    fresh_manager.check_in(student_id, course_id, timestamp=today)

    assert len(fresh_manager.attendance_log) == 1
    assert fresh_manager.attendance_log[0]["student_id"] == student_id
    assert fresh_manager.attendance_log[0]["course_id"] == course_id
    assert fresh_manager.attendance_log[0]["timestamp"] == today.isoformat()

def test_check_in_duplicate(fresh_manager):
    student_id = fresh_manager.add_student("Bob")
    teacher_id = fresh_manager.add_teacher("James", "Guitar")
    course_id = fresh_manager.add_course("Guitar", "Guitar", teacher_id)
    fresh_manager.enrol_student(student_id, course_id)
    today = dt.datetime.now()
    fresh_manager.check_in(student_id, course_id, timestamp=today)
    duplicate = fresh_manager.check_in(student_id, course_id, timestamp=today)

    assert duplicate == False
    assert len(fresh_manager.attendance_log) == 1

def test_check_in_not_enrolled(fresh_manager):
    student_id = fresh_manager.add_student("Bob")
    teacher_id = fresh_manager.add_teacher("James", "Guitar")
    course_id = fresh_manager.add_course("Guitar", "Guitar", teacher_id)
    today = dt.datetime.now()
    check_in = fresh_manager.check_in(student_id, course_id, timestamp=today)

    assert check_in == False
    assert len(fresh_manager.attendance_log) == 0

def test_check_in_invalid_student(fresh_manager):
    teacher_id = fresh_manager.add_teacher("James", "Guitar")
    course_id = fresh_manager.add_course("Guitar", "Guitar", teacher_id)
    today = dt.datetime.now()
    check_in = fresh_manager.check_in(1, course_id, timestamp=today)

    assert check_in == False
    assert len(fresh_manager.attendance_log) == 0

def test_check_in_invalid_course(fresh_manager):
    student_id = fresh_manager.add_student("Bob")
    today = dt.datetime.now()
    check_in = fresh_manager.check_in(student_id, 1, timestamp=today)

    assert check_in == False
    assert len(fresh_manager.attendance_log) == 0

def test_check_in_invalid_timestamp(fresh_manager):
    student_id = fresh_manager.add_student("Bob")
    teacher_id = fresh_manager.add_teacher("James", "Guitar")
    course_id = fresh_manager.add_course("Guitar", "Guitar", teacher_id)
    fresh_manager.enrol_student(student_id, course_id)
    check_in = fresh_manager.check_in(student_id, course_id, timestamp="dasd")

    assert check_in == True
    assert len(fresh_manager.attendance_log) == 1
    # Checks if the check in date is today's date
    assert dt.datetime.fromisoformat(fresh_manager.attendance_log[0]["timestamp"]).date() == dt.date.today()

def test_remove_teacher(fresh_manager):
    teacher_id = fresh_manager.add_teacher("James", "Guitar")
    fresh_manager.add_course("Guitar", "Guitar", teacher_id)
    fresh_manager.remove_teacher(teacher_id)

    assert len(fresh_manager.teachers) == 0
    assert fresh_manager.courses[0].teacher_id is None

def test_remove_student_invalid_teacher(fresh_manager):
    remove = fresh_manager.remove_teacher(123)

    assert remove == False

def test_remove_teacher_multiple_course(fresh_manager):
    teacher_id = fresh_manager.add_teacher("James", "Guitar")
    fresh_manager.add_course("Guitar", "Guitar", teacher_id)
    fresh_manager.add_course("Piano", "Piano", teacher_id)
    fresh_manager.remove_teacher(teacher_id)

    assert fresh_manager.courses[0].teacher_id is None
    assert fresh_manager.courses[0].teacher_id is None

def test_remove_course(fresh_manager):
    student_id = fresh_manager.add_student("Bob")
    teacher_id = fresh_manager.add_teacher("James", "Guitar")
    course_id = fresh_manager.add_course("Guitar", "Guitar", teacher_id)
    fresh_manager.enrol_student(student_id, course_id)
    fresh_manager.remove_course(course_id)

    assert len(fresh_manager.courses) == 0
    assert len(fresh_manager.students[0].enrolled_courses) == 0

def test_remove_course_invalid_course(fresh_manager):
    remove = fresh_manager.remove_course(1)

    assert remove == False

def test_remove_course_multiple_student(fresh_manager):
    student_1 = fresh_manager.add_student("Bob")
    student_2 = fresh_manager.add_student("Adam")
    teacher_id = fresh_manager.add_teacher("James", "Guitar")
    course_id = fresh_manager.add_course("Guitar", "Guitar", teacher_id)
    fresh_manager.enrol_student(student_1, course_id)
    fresh_manager.enrol_student(student_2, course_id)
    fresh_manager.remove_course(course_id)

    assert len(fresh_manager.students[0].enrolled_courses) == 0
    assert len(fresh_manager.students[1].enrolled_courses) == 0

def test_add_lesson(fresh_manager):
    teacher_id = fresh_manager.add_teacher("James", "Guitar")
    course_id = fresh_manager.add_course("Guitar", "Guitar", teacher_id)
    lesson_day = "Monday"
    start_time = "8:00"
    room = "Room A"
    lesson_id = fresh_manager.add_lesson(course_id, lesson_day, start_time, room)

    assert len(fresh_manager.courses[0].lessons) == 1
    assert fresh_manager.courses[0].lessons[0]["lesson_id"] == lesson_id
    assert fresh_manager.courses[0].lessons[0]["day"] == lesson_day
    assert fresh_manager.courses[0].lessons[0]["start_time"] == start_time
    assert fresh_manager.courses[0].lessons[0]["room"] == room

def test_add_lesson_invalid_course(fresh_manager):
    result = fresh_manager.add_lesson(1, "Monday", "1:00", "Room A")

    assert result == False

def test_add_lesson_invalid_day(fresh_manager):
    teacher_id = fresh_manager.add_teacher("James", "Guitar")
    course_id = fresh_manager.add_course("Guitar", "Guitar", teacher_id)
    result = fresh_manager.add_lesson(course_id, "asdosa", "1:00", "Room A")

    assert result == False

def test_add_lesson_invalid_start_time(fresh_manager):
    teacher_id = fresh_manager.add_teacher("James", "Guitar")
    course_id = fresh_manager.add_course("Guitar", "Guitar", teacher_id)
    result = fresh_manager.add_lesson(course_id, "Monday", "1:1231sada00", "Room A")

    assert result == False

def test_add_lesson_room_empty(fresh_manager):
    teacher_id = fresh_manager.add_teacher("James", "Guitar")
    course_id = fresh_manager.add_course("Guitar", "Guitar", teacher_id)
    result = fresh_manager.add_lesson(course_id, "Monday", "1:00", "    ")

    assert result == False

def test_daily_roster(fresh_manager):
    teacher_id = fresh_manager.add_teacher("James", "Guitar")
    course_id = fresh_manager.add_course("Guitar", "Guitar", teacher_id)
    lesson_day = "Monday"
    start_time = "8:00"
    room = "Room A"
    lesson_id = fresh_manager.add_lesson(course_id, lesson_day, start_time, room)
    lessons = fresh_manager.daily_roster("Monday")

    assert len(lessons) == 1
    assert lessons[0]["Course"] == fresh_manager.courses[0].name
    assert lessons[0]["Lesson id"] == lesson_id
    assert lessons[0]["Teacher"] == fresh_manager.teachers[0].name
    assert lessons[0]["Time"] == start_time
    assert lessons[0]["Room"] == room

def test_daily_roster_no_matching(fresh_manager):
    teacher_id = fresh_manager.add_teacher("James", "Guitar")
    course_id = fresh_manager.add_course("Guitar", "Guitar", teacher_id)
    lesson_day = "Monday"
    start_time = "8:00"
    room = "Room A"
    fresh_manager.add_lesson(course_id, lesson_day, start_time, room)
    lessons = fresh_manager.daily_roster("Tuesday")

    assert lessons is None

def test_daily_roster_no_courses(fresh_manager):
    lessons = fresh_manager.daily_roster("Monday")

    assert lessons is None

def test_daily_roster_invalid_day(fresh_manager):
    teacher_id = fresh_manager.add_teacher("James", "Guitar")
    course_id = fresh_manager.add_course("Guitar", "Guitar", teacher_id)
    lesson_day = "Monday"
    start_time = "8:00"
    room = "Room A"
    fresh_manager.add_lesson(course_id, lesson_day, start_time, room)
    lessons = fresh_manager.daily_roster("ADada")

    assert lessons == False

def test_record_payment(fresh_manager):
    student_id = fresh_manager.add_student("Bob")
    record_id = fresh_manager.record_payment(student_id, 100, "Card")

    assert len(fresh_manager.finance_log) == 1
    assert fresh_manager.finance_log[0]["id"] == record_id
    assert fresh_manager.finance_log[0]["student_id"] == student_id
    assert fresh_manager.finance_log[0]["amount"] == 100.0
    assert fresh_manager.finance_log[0]["method"] == "Card"

def test_record_payment_invalid_student(fresh_manager):
    result = fresh_manager.record_payment(1, 100, "Card")

    assert result == False

def test_record_payment_invalid_amount(fresh_manager):
    student_id = fresh_manager.add_student("Bob")
    result = fresh_manager.record_payment(student_id, "abc", "Card")

    assert result == False

def test_record_payment_empty_method(fresh_manager):
    student_id = fresh_manager.add_student("Bob")
    fresh_manager.record_payment(student_id, 100, " ")

    assert len(fresh_manager.finance_log)== 1
    assert fresh_manager.finance_log[0]["method"] == "NONE"

def test_get_payment_history(fresh_manager):
    student_id = fresh_manager.add_student("Bob")
    fresh_manager.record_payment(student_id, 100, "Card")
    payments = fresh_manager.get_payment_history(student_id)

    assert len(payments) == 1
    assert payments[0] == fresh_manager.finance_log[0]

def test_get_payment_history_no_history(fresh_manager):
    student_id = fresh_manager.add_student("Bob")
    payments = fresh_manager.get_payment_history(student_id)

    assert len(payments) == 0

def test_get_payment_history_invalid_student(fresh_manager):
    payments = fresh_manager.get_payment_history(123)

    assert len(payments) == 0

def test_find_by_id(fresh_manager):
    student_id = fresh_manager.add_student("Bob")
    teacher_id = fresh_manager.add_teacher("James", "Guitar")
    course_id = fresh_manager.add_course("Guitar", "Guitar", teacher_id)

    student_search = fresh_manager.find_by_id(student_id, search="student")
    teacher_search = fresh_manager.find_by_id(teacher_id, search="teacher")
    course_search = fresh_manager.find_by_id(course_id, search="course")

    assert student_search == fresh_manager.students[0]
    assert teacher_search == fresh_manager.teachers[0]
    assert course_search == fresh_manager.courses[0]

def test_find_by_id_no_result(fresh_manager):
    search = fresh_manager.find_by_id(1)

    assert search is None

def test_find_by_id_invalid_search(fresh_manager):
    with pytest.raises(Exception):
        fresh_manager.find_by_id(1, search="abc")

def test_register_student(fresh_manager):
    teacher_id = fresh_manager.add_teacher("James", "Guitar")
    course_id = fresh_manager.add_course("Guitar", "Guitar", teacher_id)
    student_name = "Bob"
    fresh_manager.register_student(student_name, course_id)

    assert len(fresh_manager.students) == 1
    assert fresh_manager.students[0].enrolled_courses[0] == course_id
    assert fresh_manager.courses[0].enrolled_students[0] == fresh_manager.students[0].id

def test_register_student_invalid_course(fresh_manager):
    student_name = "Bob"
    register = fresh_manager.register_student(student_name, 1)

    assert register == False
    assert len(fresh_manager.students) == 0

def test_switch_course(fresh_manager):
    student_id = fresh_manager.add_student("Bob")
    teacher_id = fresh_manager.add_teacher("James", "Guitar")
    course_id_1 = fresh_manager.add_course("Guitar", "Guitar", teacher_id)
    course_id_2 = fresh_manager.add_course("Piano", "Piano", teacher_id)

    fresh_manager.enrol_student(student_id, course_id_1)
    fresh_manager.switch_course(student_id, course_id_1, course_id_2)

    assert len(fresh_manager.students[0].enrolled_courses) == 1
    assert fresh_manager.students[0].enrolled_courses[0] != course_id_1
    assert fresh_manager.students[0].enrolled_courses[0] == course_id_2
    assert len(fresh_manager.courses[0].enrolled_students) == 0
    assert len(fresh_manager.courses[1].enrolled_students) == 1
    assert fresh_manager.courses[1].enrolled_students[0] == student_id

def test_switch_course_same_course(fresh_manager):
    student_id = fresh_manager.add_student("Bob")
    teacher_id = fresh_manager.add_teacher("James", "Guitar")
    course_id = fresh_manager.add_course("Guitar", "Guitar", teacher_id)
    fresh_manager.enrol_student(student_id, course_id)
    switch = fresh_manager.switch_course(student_id, course_id, course_id)

    assert switch == False
    assert len(fresh_manager.students[0].enrolled_courses) == 1
    assert fresh_manager.students[0].enrolled_courses[0] == course_id
    assert len(fresh_manager.courses[0].enrolled_students) == 1
    assert fresh_manager.courses[0].enrolled_students[0] == student_id

def test_switch_course_not_enrolled(fresh_manager):
    student_id = fresh_manager.add_student("Bob")
    teacher_id = fresh_manager.add_teacher("James", "Guitar")
    course_id_1 = fresh_manager.add_course("Guitar", "Guitar", teacher_id)
    course_id_2 = fresh_manager.add_course("Piano", "Piano", teacher_id)
    switch = fresh_manager.switch_course(student_id, course_id_1, course_id_2)

    assert switch == False
    assert len(fresh_manager.students[0].enrolled_courses) == 0
    assert len(fresh_manager.courses[1].enrolled_students) == 0

def test_switch_course_already_enrolled(fresh_manager):
    student_id = fresh_manager.add_student("Bob")
    teacher_id = fresh_manager.add_teacher("James", "Guitar")
    course_id_1 = fresh_manager.add_course("Guitar", "Guitar", teacher_id)
    course_id_2 = fresh_manager.add_course("Piano", "Piano", teacher_id)
    fresh_manager.enrol_student(student_id, course_id_1)
    fresh_manager.enrol_student(student_id, course_id_2)
    switch = fresh_manager.switch_course(student_id, course_id_1, course_id_2)

    assert switch == False
    assert len(fresh_manager.students[0].enrolled_courses) == 2

def test_switch_course_invalid_course(fresh_manager):
    student_id = fresh_manager.add_student("Bob")
    switch = fresh_manager.switch_course(student_id, 1, 2)

    assert switch == False
    assert len(fresh_manager.students[0].enrolled_courses) == 0
