from typing import Annotated
from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from server.settings import templates
from db.fetchers.subject import fetch_subjects, fetch_subject_by_id
from db.services import get_or_create_new_subject
from server.models import SubjectForm

router = APIRouter(prefix="/subject")


@router.get("/list/", response_class=HTMLResponse)
def subjects(request: Request) -> HTMLResponse:
    subjects = fetch_subjects()
    return templates.TemplateResponse(
        request=request,
        name="subject_list.html",
        context={"subjects": subjects, "title": "subjects"},
    )


@router.get("/show/{subject_id}/", response_class=HTMLResponse)
def show_subject(request: Request, subject_id: int) -> HTMLResponse:
    subject = fetch_subject_by_id(id=subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return templates.TemplateResponse(
        request=request,
        name="subject.html",
        context={"subject": subject, "title": subject.name},
    )


@router.get("/new/", response_class=HTMLResponse)
def new_subject_get(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="subject_new.html",
        context={"title": "New course"},
    )


@router.post("/new/", response_class=HTMLResponse)
def new_subject_post(
    request: Request, data: Annotated[SubjectForm, Form()]
) -> RedirectResponse:
    subject, _ = get_or_create_new_subject(data.name)
    return RedirectResponse(f"/show/{subject.id}", status_code=302)
