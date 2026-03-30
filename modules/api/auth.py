from fastapi import APIRouter, Response, Cookie, Request, Form
from typing import Annotated
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from modules.auth import Auth

auth_router = APIRouter()

# Авторизация
auth = Auth()

templates = Jinja2Templates(directory="templates")

# Авторизация
@auth_router.get("/")
def auth_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("auth.html", {"request": request})

@auth_router.post("/auth")
def auth_api(request: Request, response: Response, username: Annotated[str, Form()], password: Annotated[str, Form()]):
    '''
    Авторизация
    В случае успеха выдается session_id
    '''

    if request.cookies.get("session_id"):
        isAuth, role, username = auth.checkAuth(request.cookies.get("session_id"))
        if isAuth:
            return {"message": "Вы уже авторизованы", "role": role}
    
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
        return {"message": "Авторизация неуспешна"}