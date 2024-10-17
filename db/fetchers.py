from sqlalchemy.orm import Session
from sqlalchemy import select
from db import engine
from db.models import Student, Сourse, Subject


def fetch_students():
    session = Session(engine)
    return session.scalars(select(Student))


def fetch_courses():
    session = Session(engine)
    return session.scalars(select(Сourse))


def fetch_course_by_id(id: int):
    session = Session(engine)
    return session.scalars(select(Сourse).where(Сourse.id == id)).one()


def fetch_subjects():
    session = Session(engine)
    return session.scalars(select(Subject))
