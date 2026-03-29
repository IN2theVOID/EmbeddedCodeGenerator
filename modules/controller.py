from urllib import response

from fastapi.responses import HTMLResponse

from fastapi import FastAPI, Response, Cookie, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated, List

from modules.auth import Auth
from modules.database import Audit, Info
from modules.llm import Llm
from modules.deploy import DeployToDevice

# Создаем контроллер API
controller = FastAPI()

templates = Jinja2Templates(directory="templates")

# Авторизация
auth = Auth()



@controller.post("/auth")
def auth_api(request: Request, response: Response, username: Annotated[str, Form()], password: Annotated[str, Form()]):
    '''
    Авторизация
    В случае успеха выдается session_id
    '''

    if request.cookies.get("session_id"):
        isAuth, role, username = auth.checkAuth(request.cookies.get("session_id"))
        print(isAuth)
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

# Авторизация
@controller.get("/")
def auth_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("auth.html", {"request": request})

# Консоль администратора
@controller.get("/admin_console")
def admin_console(request: Request) -> HTMLResponse:
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
    return {"message": "Вы не авторизованы!"}

# Дашборд
@controller.get("/dashboard")
def dashboard(request: Request) -> HTMLResponse:
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
    return {"message": "Вы не авторизованы!"}

# Генератор (страница)
@controller.get("/code_generator")
def emb_code_gen_form(request: Request) -> HTMLResponse:
    if request.cookies.get("session_id"):
        isAuth, role, username = auth.checkAuth(request.cookies.get("session_id"))
        if isAuth and role == "user":
            info = Info()

            languages = info.get_records("languages", "label")
            platforms = info.get_records("platforms", "label")
            models = info.get_records("models", "label")

            return templates.TemplateResponse("generator.html", {"request":     request, 
                                                                "name":         username,
                                                                "languages":    languages,
                                                                "platforms":    platforms,
                                                                "models":       models})
    return {"message": "Вы не авторизованы!"}

# Развертывание (страница)
@controller.get("/deploy")
def deploy_form(request: Request) -> HTMLResponse:
    if request.cookies.get("session_id"):
        isAuth, role, username = auth.checkAuth(request.cookies.get("session_id"))
        if isAuth and role == "user":
            info = Info()
            
            devices = info.get_records("devices", "label,address,type")
            device_types = info.get_records("device_type", "label")
            generations = info.get_records("generations", "task,code")

            return templates.TemplateResponse("deploy.html", {"request":             request, 
                                                                "name":                 username,
                                                                "devices":              devices,
                                                                "device_types":         device_types,
                                                                "generations":          generations})
    return {"message": "Вы не авторизованы!"}

# Развертывание (api)
@controller.post("/deploy")
def deploy_api(
    request: Request,
    devices: List[str] = Form(...),      # Получаем список выбранных устройств
    generation: str = Form(...)          # Получаем выбранную генерацию (код)
):
    # try:
    deploy = DeployToDevice()
    print(f"Получен запрос на установку!")
    print(f"Выбранные устройства: {devices}")
    print(f"Код генерации: {generation}")

    response = deploy.deploy(devices=devices, generation=generation)

    # except:
    #     return {"message": "Ошибка установки!"}  
    # return {"message": "Установка кода '" + str(generation) + "' на устройства '" + str(devices) + "' успешно выполнена!"} 
    return {"message": response}

@controller.get("/audit")
def audit_form(request: Request) -> HTMLResponse:
    if request.cookies.get("session_id"):
        isAuth, role, username = auth.checkAuth(request.cookies.get("session_id"))
        if isAuth and role == "auditor":
            audit = Audit()
            auditRecords = audit.get_all_records()
            return templates.TemplateResponse(
                "audit.html", {"request": request, 
                               "name": username, 
                               "message": auditRecords})
    return {"message": "Вы не авторизованы!"}   

# Обработчик GET-запросов, апи генератора
@controller.get("/emb_code_gen", response_class=HTMLResponse)
async def generate_code(request: Request, language: str, platform: str, task: str, model: str) -> HTMLResponse:
    if request.cookies.get("session_id"):
        isAuth, role, username = auth.checkAuth(request.cookies.get("session_id"))
        if isAuth and role == "user":
            llm = Llm()
            audit = Audit()
            audit.add_record(username=username, record="Generation: " + language + " " + platform + " " + task)
            
            html_content = llm.generate_code(language=language,
                                             platform=platform,
                                             task=task,
                                             model=model)
            
            return HTMLResponse(content=html_content, 
                                status_code=200)