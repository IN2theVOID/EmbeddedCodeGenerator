from fastapi.responses import HTMLResponse
from fastapi import  Request, APIRouter

from modules.auth import Auth
from modules.database import Audit
from modules.api.templating import templateInfoMessage, templates

audit_router = APIRouter()

# Аутентификация
auth = Auth()

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