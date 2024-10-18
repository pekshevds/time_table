from typing import Iterable
from sqlalchemy import select
from db import session
from db.models import Course
from db.fetchers.base import fetch_instance_by


def fetch_courses() -> Iterable[Course]:
    return session.scalars(select(Course))


def fetch_course_by_id(id: int) -> Course | None:
    return fetch_instance_by(Course, "id", id)


def fetch_course_by_name(name: str) -> Course | None:
    return fetch_instance_by(Course, "name", name)
