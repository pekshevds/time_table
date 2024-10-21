from typing import Annotated
from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from server.settings import templates
from db.fetchers.student import fetch_student_by_id
from db.fetchers.subject import fetch_subject_by_id
from db.services import create_or_update_record
from server.models import RecordForm

router = APIRouter(prefix="/record")


@router.get("/new/{student_id}/{subject_id}/", response_class=HTMLResponse)
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


@router.post("/new/", response_class=HTMLResponse)
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
