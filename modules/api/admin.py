from fastapi import APIRouter, Request, Form
from typing import Annotated
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse

from modules.auth import Auth
from modules.database import DbRecords

admin_router = APIRouter()

# Аутентификация
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
            info = DbRecords()
            
            users = info.get_info(table="users", columns="username")
            roles = info.get_info(table="roles", columns="username, role")
            languages = info.get_info(table="languages", columns="label")
            platforms = info.get_info(table="platforms", columns="label")
            models = info.get_info(table="models", columns="label")
            devices = info.get_info(table="devices", columns="label,address")

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