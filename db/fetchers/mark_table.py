from typing import Iterable
from sqlalchemy import select
from db import session
from db.models import MarkTable, Student, Subject, Course


def fetch_mark_table_by_course(course: Course) -> Iterable[MarkTable]:
    statement = select(MarkTable).where(MarkTable.student.course == course)
    return session.scalars(statement).all()


def fetch_record(student: Student, subject: Subject) -> MarkTable | None:
    statement = select(MarkTable).where(
        (MarkTable.student == student) & (MarkTable.subject == subject)
    )
    return session.scalars(statement).first()
