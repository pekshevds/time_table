from typing import Iterable
from sqlalchemy import select
from db import session
from db.models import Student
from db.fetchers.base import fetch_instance_by


def fetch_students() -> Iterable[Student]:
    return session.scalars(select(Student).order_by(Student.name.asc())).all()


def fetch_student_by_id(id: int) -> Student | None:
    return fetch_instance_by(Student, "id", id)


def fetch_student_by_name(name: str) -> Student | None:
    return fetch_instance_by(Student, "name", name)
