from fastapi import FastAPI

from modules.api.auth import auth_router
from modules.api.admin import admin_router
from modules.api.dashboard import dashboard_router
from modules.api.generator import generator_router
from modules.api.audit import audit_router


# Создаем контроллер API
controller = FastAPI()

# Наполянем роутерами
controller.include_router(auth_router)
controller.include_router(admin_router)
controller.include_router(dashboard_router)
controller.include_router(generator_router)
controller.include_router(audit_router)
