import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from server.settings import templates
from server.routers.course import router as course_router
from server.routers.subject import router as subject_router
from server.routers.student import router as student_router
from server.routers.mark_table import router as record_router


app = FastAPI()
app.include_router(course_router)
app.include_router(subject_router)
app.include_router(student_router)
app.include_router(record_router)


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"title": "index"},
    )


if __name__ == "__main__":
    uvicorn.run(app)
