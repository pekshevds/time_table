from typing import Iterable
from sqlalchemy import select
from db import session
from db.models import Student


def fetch_students() -> Iterable[Student]:
    return session.scalars(select(Student))
