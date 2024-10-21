from typing import Annotated
from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from server.settings import templates
from db.fetchers.course import fetch_courses, fetch_course_by_id
from db.fetchers.mark_table import fetch_full_mark_table_by_course
from db.services import get_or_create_new_course
from server.models import СourseForm

router = APIRouter(prefix="/course")


@router.get("/list/", response_class=HTMLResponse)
def courses(request: Request) -> HTMLResponse:
    courses = fetch_courses()
    return templates.TemplateResponse(
        request=request,
        name="course_list.html",
        context={"courses": courses, "title": "index"},
    )


@router.get("/show/{course_id}/", response_class=HTMLResponse)
def show_course(request: Request, course_id: int) -> HTMLResponse:
    course = fetch_course_by_id(id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    table = fetch_full_mark_table_by_course(course=course)
    return templates.TemplateResponse(
        request=request,
        name="course.html",
        context={"table": table, "title": course.name},
    )


@router.get("/new/", response_class=HTMLResponse)
def new_course_get(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="course_new.html",
        context={"title": "New course"},
    )


@router.post("/new/", response_class=HTMLResponse)
def new_course_post(
    request: Request, data: Annotated[СourseForm, Form()]
) -> RedirectResponse:
    course, _ = get_or_create_new_course(data.name)
    return RedirectResponse(f"/show/{course.id}", status_code=302)
