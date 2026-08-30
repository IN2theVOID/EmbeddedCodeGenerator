from fastapi.responses import HTMLResponse
from fastapi import  Request, Form, APIRouter
from typing import List

from prometheus_client import Counter

from modules.auth import Auth
from modules.database import Audit, DbRecords

from modules.deploy import DeployToDevice
from modules.exceptions import DeployError
from modules.logger import log
from modules.api.templating import templateInfoMessage, templates

deploy_router = APIRouter()

# Аутентификация
auth = Auth()

# Prometheus метрики
prometheus_deploy_metric = Counter("deployments", "Code deployments count")

# Развертывание (страница)
@deploy_router.get("/deploy")
def deploy_form(request: Request) -> HTMLResponse:
    '''
    Развертывание (страница)
    '''
    if request.cookies.get("session_id"):
        isAuth, role, username = auth.checkAuth(request.cookies.get("session_id"))
        if isAuth and role == "user":
            info = DbRecords()
            
            devices = info.get_info(table="devices", columns="label,address,type")
            device_types = info.get_info(table="device_type", columns="label")
            generations = info.get_info(table="generations", columns="task,code")

            return templates.TemplateResponse("deploy.html", {
                "request":             request, 
                "name":                 username,
                "devices":              devices,
                "device_types":         device_types,
                "generations":          generations,
                }
            )
    return templateInfoMessage("Вы не авторизованы!", request)

# Развертывание (api)
@deploy_router.post("/deploy")
def deploy_api(
    request: Request,
    devices: List[str] = Form(...),      # Получаем список выбранных устройств
    generation: str = Form(...),         # Получаем выбранную генерацию (код)
):
    '''
    Развертывание (api)
    '''
    if request.cookies.get("session_id"):
        isAuth, role, username = auth.checkAuth(request.cookies.get("session_id"))
        if isAuth and role == "user":
            deploy = DeployToDevice()
            audit = Audit()
            audit.add_record(username=username, record="Deploy: " + str(devices) + " " + generation[:15])
            log.info("Получен запрос на установку!")
            log.info(f"Выбранные устройства: {devices}")
            log.info(f"Код генерации: {generation}")
            try:
                response = deploy.deploy(devices=devices, generation=generation)
                prometheus_deploy_metric.inc()
            except DeployError:
                return templateInfoMessage(f"Ошибка разворачивания на {devices}!", request)
            
            return templateInfoMessage(response, request)
    return templateInfoMessage("Вы не авторизованы!", request)

