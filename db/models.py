from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String, Integer, Date, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Subject(Base):
    __tablename__ = "subject"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    marks: Mapped[List["MarkTable"]] = relationship(
        back_populates="subject", cascade="all, delete-orphan"
    )

    def __str__(self) -> str:
        return f"Subject ({self.name})"


class Сourse(Base):
    __tablename__ = "course"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    students: Mapped[List["Student"]] = relationship(
        back_populates="course", cascade="all, delete-orphan"
    )

    def __str__(self) -> str:
        return f"Сourse ({self.name})"


class Student(Base):
    __tablename__ = "student"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    fullname: Mapped[Optional[str]]
    marks: Mapped[List["MarkTable"]] = relationship(
        back_populates="student", cascade="all, delete-orphan"
    )
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id"))
    course: Mapped["Сourse"] = relationship(back_populates="students")

    def __str__(self) -> str:
        return f"Student ({self.id}, {self.name})"


class MarkTable(Base):
    __tablename__ = "mark_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(Date)
    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"))
    student: Mapped["Student"] = relationship(back_populates="marks")
    subject_id: Mapped[int] = mapped_column(ForeignKey("subject.id"))
    subject: Mapped["Subject"] = relationship(back_populates="marks")
    mark: Mapped[int] = mapped_column(Integer)

    def __str__(self) -> str:
        return f"Student ({self.id}, {self.name})"


__all__ = (
    "Base",
    "Subject",
    "Сourse",
    "Student",
    "MarkTable",
)
