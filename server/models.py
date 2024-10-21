from pydantic import BaseModel


class СourseForm(BaseModel):
    name: str


class SubjectForm(BaseModel):
    name: str


class StudentForm(BaseModel):
    name: str
    course: int
