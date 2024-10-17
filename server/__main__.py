import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db.fetchers import fetch_courses, fetch_course_by_id


app = FastAPI()
templates = Jinja2Templates(directory="server/templates")


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    courses = fetch_courses()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"courses": courses, "title": "index"},
    )


@app.get("/course/{course_id}", response_class=HTMLResponse)
def course_list(request: Request, course_id: int):
    print(course_id)
    course = fetch_course_by_id(id=course_id)
    return templates.TemplateResponse(
        request=request,
        name="course_list.html",
        context={"course": course, "title": course.name},
    )


if __name__ == "__main__":
    uvicorn.run(app)
