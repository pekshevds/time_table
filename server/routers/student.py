from typing import Annotated
from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from server.settings import templates
from db.fetchers.course import fetch_courses, fetch_course_by_id
from db.fetchers.student import fetch_students, fetch_student_by_id
from db.services import get_or_create_new_student
from server.models import StudentForm

router = APIRouter(prefix="/student")


@router.get("/list/", response_class=HTMLResponse)
def students(request: Request) -> HTMLResponse:
    students = fetch_students()
    return templates.TemplateResponse(
        request=request,
        name="student_list.html",
        context={"students": students, "title": "students"},
    )


@router.get("/show/{student_id}/", response_class=HTMLResponse)
def show_student(request: Request, student_id: int) -> HTMLResponse:
    student = fetch_student_by_id(id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return templates.TemplateResponse(
        request=request,
        name="student.html",
        context={"student": student, "title": student.name},
    )


@router.get("/new/", response_class=HTMLResponse)
def new_student_get(request: Request) -> HTMLResponse:
    courses = fetch_courses()
    return templates.TemplateResponse(
        request=request,
        name="student_new.html",
        context={"courses": courses, "title": "New ctudent"},
    )


@router.post("/new/", response_class=HTMLResponse)
def new_student_post(
    request: Request, data: Annotated[StudentForm, Form()]
) -> RedirectResponse:
    course = fetch_course_by_id(data.course)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    student, _ = get_or_create_new_student(data.name, course=course)
    return RedirectResponse(f"/student/show/{student.id}", status_code=302)
