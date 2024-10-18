from typing import Annotated
import uvicorn
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db.fetchers.course import fetch_courses, fetch_course_by_id
from db.services import get_or_create_new_course
from server.models import СourseForm

app = FastAPI()
templates = Jinja2Templates(directory="server/templates")


@app.get("/", response_class=HTMLResponse)
def root(request: Request) -> HTMLResponse:
    courses = fetch_courses()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"courses": courses, "title": "index"},
    )


@app.get("/course/show/{course_id}", response_class=HTMLResponse)
def course_list(request: Request, course_id: int) -> HTMLResponse:
    course = fetch_course_by_id(id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return templates.TemplateResponse(
        request=request,
        name="course_list.html",
        context={"course": course, "title": course.name},
    )


@app.get("/course/new", response_class=HTMLResponse)
def course_new_get(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="course_new.html",
        context={"title": "New course"},
    )


@app.post("/course/new", response_class=HTMLResponse)
def course_new_post(
    request: Request, data: Annotated[СourseForm, Form()]
) -> RedirectResponse:
    course, _ = get_or_create_new_course(data.name)
    return RedirectResponse(f"/course/show/{course.id}", status_code=302)


if __name__ == "__main__":
    uvicorn.run(app)
