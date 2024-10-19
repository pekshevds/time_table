from db import session
from db.fetchers.course import fetch_course_by_name
from db.fetchers.subject import fetch_subject_by_name
from db.models import Student, Course, Subject


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
