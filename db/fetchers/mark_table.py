from typing import Iterable, List
from pydantic import BaseModel, Field
from sqlalchemy import select
from db import session
from db.models import MarkTable, Student, Subject, Course
from db.fetchers.subject import fetch_subjects


class PStudent(BaseModel):
    id: int
    name: str


class PSubject(BaseModel):
    id: int
    name: str


class Mark(BaseModel):
    subject: PSubject
    mark: int = 0


class Row(BaseModel):
    student: PStudent
    marks: List[Mark] = Field(default_factory=list)


class Table(BaseModel):
    header: list[PSubject] = Field(default_factory=list)
    body: List[Row] = Field(default_factory=list)


def fetch_mark_table_by_course(course: Course) -> Iterable[MarkTable]:
    statement = select(MarkTable).where(MarkTable.student.course == course)
    return session.scalars(statement).all()


def fetch_record(student: Student, subject: Subject) -> MarkTable | None:
    statement = select(MarkTable).where(
        (MarkTable.student == student) & (MarkTable.subject == subject)
    )
    return session.scalars(statement).first()


def fetch_full_mark_table_by_course(course: Course) -> Table:
    statement = select(MarkTable).where(Student.course == course)
    mark_table = session.scalars(statement).all()
    subjects = fetch_subjects()
    header = []
    for subject in subjects:
        header.append(PSubject(id=subject.id, name=subject.name))
    rows = []
    for student in course.students:
        marks = []
        for subject in subjects:
            mark = 0
            for record in mark_table:
                if record.student == student and record.subject == subject:
                    mark = record.mark
                    break
            mark = Mark(subject=PSubject(id=subject.id, name=subject.name), mark=mark)
            marks.append(mark)
        row = Row(student=PStudent(id=student.id, name=student.name), marks=marks)
        rows.append(row)
    table = Table(body=rows, header=header)
    return table
