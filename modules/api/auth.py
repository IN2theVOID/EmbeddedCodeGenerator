from fastapi import APIRouter, Response, Cookie, Request, Form
from typing import Annotated
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from modules.auth import Auth

auth_router = APIRouter()

# Аутентификация
auth = Auth()

templates = Jinja2Templates(directory="templates")

# Аутентификация
@auth_router.get("/")
def auth_page(request: Request) -> HTMLResponse:
    '''
    Форма авторизации
    '''
    return templates.TemplateResponse("auth.html", {"request": request})

@auth_router.post("/auth")
def auth_api(request: Request, response: Response, username: Annotated[str, Form()], password: Annotated[str, Form()]):
    '''
    API Авторизации
    В случае успеха выдается session_id
    '''

    if request.cookies.get("session_id"):
        isAuth, role, username = auth.checkAuth(request.cookies.get("session_id"))
        if isAuth:
            return templateInfoMessage(f"Вы уже авторизованы! Роль: {role}", request)
    
    authResponse = auth.authUser(username, password)
    if authResponse.isAuth:
        response = RedirectResponse(url="/", status_code=303)
        match auth.getRoleFromToken(authResponse.cookieString):
            case "user":
                response = RedirectResponse(url="/code_generator", status_code=303)
            case "admin":
                response = RedirectResponse(url="/admin_console", status_code=303)
            case "auditor":
                response = RedirectResponse(url="/audit", status_code=303)
            case "viewer":
                response = RedirectResponse(url="/dashboard", status_code=303)
        response.set_cookie(key="session_id", value=authResponse.cookieString)
        return response
    else:
        return templateInfoMessage("Аутентификация неуспешна!", request)

def templateInfoMessage(message: str, request: Request) -> _TemplateResponse:
    return templates.TemplateResponse(
                "message.html", {"request": request, 
                                 "message": message})