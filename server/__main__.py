from typing import Annotated
import uvicorn
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db.fetchers.course import fetch_courses, fetch_course_by_id
from db.fetchers.subject import fetch_subjects, fetch_subject_by_id
from db.services import get_or_create_new_course, get_or_create_new_subject
from server.models import СourseForm, SubjectForm

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


@app.get("/course/show/{course_id}", response_class=HTMLResponse)
def show_course(request: Request, course_id: int) -> HTMLResponse:
    course = fetch_course_by_id(id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return templates.TemplateResponse(
        request=request,
        name="course.html",
        context={"course": course, "title": course.name},
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


if __name__ == "__main__":
    uvicorn.run(app)
