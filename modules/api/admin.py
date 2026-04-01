from fastapi import APIRouter, Cookie, Request, Form
from typing import Annotated
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse

from modules.auth import Auth
from modules.database import Info

admin_router = APIRouter()

# Авторизация
auth = Auth()

templates = Jinja2Templates(directory="templates")

# Консоль администратора
@admin_router.get("/admin_console")
def admin_console(request: Request) -> HTMLResponse:
    '''
    Страница Консоль администратора
    '''
    if request.cookies.get("session_id"):
        isAuth, role, username = auth.checkAuth(request.cookies.get("session_id"))
        if isAuth and role == "admin":
            info = Info()
            
            users = info.get_records("users", "username")
            roles = info.get_records("roles", "username, role")
            languages = info.get_records("languages", "label")
            platforms = info.get_records("platforms", "label")
            models = info.get_records("models", "label")
            devices = info.get_records("devices", "label,address")

            return templates.TemplateResponse("admin.html", {"request":         request, 
                                                                "name":         username,
                                                                "users":        users,
                                                                "roles":        roles,
                                                                "languages":    languages,
                                                                "platforms":    platforms,
                                                                "models":       models,
                                                                "devices":      devices})
    return templateInfoMessage("Вы не авторизованы!", request)

# Создание пользователя
@admin_router.post("/create_user")
def create_user(request: Request, createusername: Annotated[str, Form()], password: Annotated[str, Form()], role: Annotated[str, Form()]):
    '''
    Создание нового пользователя
    '''
    if request.cookies.get("session_id"):
        isAuth, role, username = auth.checkAuth(request.cookies.get("session_id"))
        if isAuth and role == "admin":
            # todo
            return templateInfoMessage("Пользователь " + createusername + " успешно создан", request)
            
    return templateInfoMessage("Вы не авторизованы!", request)

def templateInfoMessage(message: str, request: Request) -> _TemplateResponse:
    return templates.TemplateResponse(
                "message.html", {"request": request, 
                                 "message": message})