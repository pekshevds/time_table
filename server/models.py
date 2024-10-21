from pydantic import BaseModel


class СourseForm(BaseModel):
    name: str


class SubjectForm(BaseModel):
    name: str


class StudentForm(BaseModel):
    name: str
    course: int


class RecordForm(BaseModel):
    student: int
    subject: int
    mark: int
