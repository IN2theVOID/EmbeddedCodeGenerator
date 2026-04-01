from fastapi.responses import HTMLResponse
from fastapi import  Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List
from starlette.templating import _TemplateResponse

from modules.auth import Auth
from modules.database import Audit, Info
from modules.llm import Llm
from modules.deploy import DeployToDevice
from modules.exceptions import ModelError, DeployError

generator_router = APIRouter()

# Авторизация
auth = Auth()

templates = Jinja2Templates(directory="templates")


# Генератор (страница)
@generator_router.get("/code_generator")
def emb_code_gen_form(request: Request) -> HTMLResponse:
    '''
    Генератор (страница)
    '''
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
    return templateInfoMessage("Вы не авторизованы!", request)


# Развертывание (страница)
@generator_router.get("/deploy")
def deploy_form(request: Request) -> HTMLResponse:
    '''
    Развертывание (страница)
    '''
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
    return templateInfoMessage("Вы не авторизованы!", request)

# Развертывание (api)
@generator_router.post("/deploy")
def deploy_api(
    request: Request,
    devices: List[str] = Form(...),      # Получаем список выбранных устройств
    generation: str = Form(...)          # Получаем выбранную генерацию (код)
):
    '''
    Развертывание (api)
    '''
    # try:
    if request.cookies.get("session_id"):
        isAuth, role, username = auth.checkAuth(request.cookies.get("session_id"))
        if isAuth and role == "user":
            deploy = DeployToDevice()
            print(f"Получен запрос на установку!")
            print(f"Выбранные устройства: {devices}")
            print(f"Код генерации: {generation}")
            try:
                response = deploy.deploy(devices=devices, generation=generation)
            except DeployError:
                return templateInfoMessage(f"Ошибка разворачивания на {devices}!", request)
            
            return templateInfoMessage(response, request)
    return templateInfoMessage("Вы не авторизованы!", request)

# Обработчик GET-запросов, апи генератора
@generator_router.get("/emb_code_gen", response_class=HTMLResponse)
async def generate_code(request: Request, language: str, platform: str, task: str, model: str) -> HTMLResponse:
    '''
    Обработчик GET-запросов, апи генератора
    '''
    if request.cookies.get("session_id"):
        isAuth, role, username = auth.checkAuth(request.cookies.get("session_id"))
        if isAuth and role == "user":
            llm = Llm()
            audit = Audit()
            audit.add_record(username=username, record="Generation: " + language + " " + platform + " " + task)
            
            try:
                html_content = llm.generate_code(language=language,
                                                platform=platform,
                                                task=task,
                                                model=model)
            except ModelError:
                return templateInfoMessage("Ошибка модели!", request)

            return HTMLResponse(content=html_content, 
                                status_code=200)
        
def templateInfoMessage(message: str, request: Request) -> _TemplateResponse:
    return templates.TemplateResponse(
                "message.html", {"request": request, 
                                 "message": message})