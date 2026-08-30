from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from modules.api.auth import auth_router
from modules.api.admin import admin_router
from modules.api.dashboard import dashboard_router
from modules.api.generator import generator_router
from modules.api.audit import audit_router
from modules.api.deploy import deploy_router
from modules.lifespan import lifespan

# Создаем контроллер API
controller = FastAPI(lifespan=lifespan)

# Наполянем контроллер роутерами
for router in [
        auth_router,
        admin_router, 
        dashboard_router,
        generator_router,
        audit_router, 
        deploy_router,
    ]:
    controller.include_router(router)

Instrumentator().instrument(controller).expose(controller)