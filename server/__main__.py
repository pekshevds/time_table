from typing import Annotated
import uvicorn
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db.fetchers.course import fetch_courses, fetch_course_by_id
from db.fetchers.subject import fetch_subjects, fetch_subject_by_id
from db.fetchers.student import fetch_students, fetch_student_by_id
from db.services import (
    get_or_create_new_course,
    get_or_create_new_subject,
    get_or_create_new_student,
    create_or_update_record,
)
from server.models import СourseForm, SubjectForm, StudentForm, RecordForm

app = FastAPI()
templates = Jinja2Templates(directory="server/templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"title": "index"},
    )


@app.get("/courses/", response_class=HTMLResponse)
def courses(request: Request) -> HTMLResponse:
    courses = fetch_courses()
    return templates.TemplateResponse(
        request=request,
        name="course_list.html",
        context={"courses": courses, "title": "index"},
    )


@app.get("/course/show/{course_id}/", response_class=HTMLResponse)
def show_course(request: Request, course_id: int) -> HTMLResponse:
    course = fetch_course_by_id(id=course_id)
    subjects = fetch_subjects()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return templates.TemplateResponse(
        request=request,
        name="course.html",
        context={"course": course, "subjects": subjects, "title": course.name},
    )


@app.get("/course/new/", response_class=HTMLResponse)
def new_course_get(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="course_new.html",
        context={"title": "New course"},
    )


@app.post("/course/new/", response_class=HTMLResponse)
def new_course_post(
    request: Request, data: Annotated[СourseForm, Form()]
) -> RedirectResponse:
    course, _ = get_or_create_new_course(data.name)
    return RedirectResponse(f"/course/show/{course.id}", status_code=302)


@app.get("/subjects/", response_class=HTMLResponse)
def subjects(request: Request) -> HTMLResponse:
    subjects = fetch_subjects()
    return templates.TemplateResponse(
        request=request,
        name="subject_list.html",
        context={"subjects": subjects, "title": "subjects"},
    )


@app.get("/subject/show/{subject_id}/", response_class=HTMLResponse)
def show_subject(request: Request, subject_id: int) -> HTMLResponse:
    subject = fetch_subject_by_id(id=subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return templates.TemplateResponse(
        request=request,
        name="subject.html",
        context={"subject": subject, "title": subject.name},
    )


@app.get("/subject/new/", response_class=HTMLResponse)
def new_subject_get(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="subject_new.html",
        context={"title": "New course"},
    )


@app.post("/subject/new/", response_class=HTMLResponse)
def new_subject_post(
    request: Request, data: Annotated[SubjectForm, Form()]
) -> RedirectResponse:
    subject, _ = get_or_create_new_subject(data.name)
    return RedirectResponse(f"/subject/show/{subject.id}", status_code=302)


@app.get("/students/", response_class=HTMLResponse)
def students(request: Request) -> HTMLResponse:
    students = fetch_students()
    return templates.TemplateResponse(
        request=request,
        name="student_list.html",
        context={"students": students, "title": "students"},
    )


@app.get("/student/show/{student_id}/", response_class=HTMLResponse)
def show_student(request: Request, student_id: int) -> HTMLResponse:
    student = fetch_student_by_id(id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return templates.TemplateResponse(
        request=request,
        name="student.html",
        context={"student": student, "title": student.name},
    )


@app.get("/student/new/", response_class=HTMLResponse)
def new_student_get(request: Request) -> HTMLResponse:
    courses = fetch_courses()
    return templates.TemplateResponse(
        request=request,
        name="student_new.html",
        context={"courses": courses, "title": "New ctudent"},
    )


@app.post("/student/new/", response_class=HTMLResponse)
def new_student_post(
    request: Request, data: Annotated[StudentForm, Form()]
) -> RedirectResponse:
    course = fetch_course_by_id(data.course)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    student, _ = get_or_create_new_student(data.name, course=course)
    return RedirectResponse(f"/student/show/{student.id}", status_code=302)


@app.get("/record/new/{student_id}/{subject_id}/", response_class=HTMLResponse)
def new_record_get(request: Request, student_id: int, subject_id: int) -> HTMLResponse:
    student = fetch_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    subject = fetch_subject_by_id(subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return templates.TemplateResponse(
        request=request,
        name="record_new.html",
        context={"student": student, "subject": subject, "title": "New record"},
    )


@app.post("/record/new/", response_class=HTMLResponse)
def new_record_post(
    request: Request, data: Annotated[RecordForm, Form()]
) -> RedirectResponse:
    student = fetch_student_by_id(data.student)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    subject = fetch_subject_by_id(data.subject)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    mark = data.mark
    create_or_update_record(student=student, subject=subject, makr=mark)
    return RedirectResponse(f"/course/show/{student.course.id}/", status_code=302)


if __name__ == "__main__":
    uvicorn.run(app)
