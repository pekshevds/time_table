from db import session
from db.fetchers.course import fetch_course_by_name
from db.fetchers.subject import fetch_subject_by_name
from db.fetchers.student import fetch_student_by_name
from db.fetchers.mark_table import fetch_record
from db.models import Student, Course, Subject, MarkTable


def get_or_create_new_course(name: str) -> tuple[Course, bool]:
    course = fetch_course_by_name(name)
    if course:
        return course, False
    course = Course(name=name)
    session.add_all([course])
    session.commit()
    return course, True


def get_or_create_new_subject(name: str) -> tuple[Subject, bool]:
    subject = fetch_subject_by_name(name)
    if subject:
        return subject, False
    subject = Subject(name=name)
    session.add_all([subject])
    session.commit()
    return subject, True


def get_or_create_new_student(name: str, course: Course) -> tuple[Student, bool]:
    student = fetch_student_by_name(name)
    if student:
        return student, False
    student = Student(name=name, course=course)
    session.add_all([student])
    session.commit()
    return student, True


def create_or_update_record(student: Student, subject: Subject, makr: int) -> None:
    record = fetch_record(student, subject)
    if not record:
        record = MarkTable(student=student, subject=subject)
    record.mark = makr
    session.commit()
