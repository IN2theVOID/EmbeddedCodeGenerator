from fastapi.responses import HTMLResponse

from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse

from modules.auth import Auth
from modules.database import Info

from modules.auth import Auth

dashboard_router = APIRouter()

# Аутентификация
auth = Auth()

templates = Jinja2Templates(directory="templates")

# Дашборд
@dashboard_router.get("/dashboard")
def dashboard(request: Request) -> HTMLResponse:
    '''
    Обзор системы
    '''
    if request.cookies.get("session_id"):
        isAuth, role, username = auth.checkAuth(request.cookies.get("session_id"))
        if isAuth and role in ["viewer", "user", "admin"]:
            info = Info()
            
            languages = info.get_records("languages", "label")
            platforms = info.get_records("platforms", "label")
            models = info.get_records("models", "label")
            devices = info.get_records("devices", "label,address,type")
            generations = info.get_records("generations", "task,code")

            return templates.TemplateResponse("dashboard.html", {"request":         request, 
                                                                "name":         username,
                                                                "languages":    languages,
                                                                "platforms":    platforms,
                                                                "models":       models,
                                                                "devices":      devices,
                                                                "generations":  generations})
    return templateInfoMessage("Вы не авторизованы!", request)

def templateInfoMessage(message: str, request: Request) -> _TemplateResponse:
    return templates.TemplateResponse(
                "message.html", {"request": request, 
                                 "message": message})