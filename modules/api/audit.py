from fastapi.responses import HTMLResponse
from fastapi import  Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List
from starlette.templating import _TemplateResponse

from modules.auth import Auth
from modules.database import Audit

audit_router = APIRouter()

# Авторизация
auth = Auth()

templates = Jinja2Templates(directory="templates")

@audit_router.get("/audit")
def audit_form(request: Request) -> HTMLResponse:
    '''
    Страница Аудит
    '''
    if request.cookies.get("session_id"):
        isAuth, role, username = auth.checkAuth(request.cookies.get("session_id"))
        if isAuth and role == "auditor":
            audit = Audit()
            auditRecords = audit.get_all_records()
            return templates.TemplateResponse(
                "audit.html", {"request": request, 
                               "name": username, 
                               "message": auditRecords})
    return templateInfoMessage("Вы не авторизованы!", request)

def templateInfoMessage(message: str, request: Request) -> _TemplateResponse:
    return templates.TemplateResponse(
                "message.html", {"request": request, 
                                 "message": message})