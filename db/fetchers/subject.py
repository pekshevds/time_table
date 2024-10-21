from typing import Iterable
from sqlalchemy import select
from db import session
from db.models import Subject
from db.fetchers.base import fetch_instance_by


def fetch_subjects() -> Iterable[Subject]:
    return session.scalars(select(Subject).order_by(Subject.name.asc())).all()


def fetch_subject_by_id(id: int) -> Subject | None:
    return fetch_instance_by(Subject, "id", id)


def fetch_subject_by_name(name: str) -> Subject | None:
    return fetch_instance_by(Subject, "name", name)
