from fastapi.responses import HTMLResponse
from fastapi import  Request, APIRouter
from prometheus_client import Counter

from modules.auth import Auth
from modules.database import Audit, DbRecords
from modules.llm import LLmFactory
from modules.exceptions import ModelError
from modules.api.templating import templateInfoMessage, templates

generator_router = APIRouter()

# Аутентификация
auth = Auth()

# Prometheus метрики
prometheus_generate_metric = Counter("generations", "Code generations count")

# Генератор (страница)
@generator_router.get("/code_generator")
def emb_code_gen_form(request: Request) -> HTMLResponse:
    '''
    Генератор (страница)
    '''
    if request.cookies.get("session_id"):
        isAuth, role, username = auth.checkAuth(request.cookies.get("session_id"))
        if isAuth and role == "user":
            info = DbRecords()

            languages = info.get_info(table="languages", columns="label")
            platforms = info.get_info(table="platforms", columns="label")
            models = info.get_info(table="models", columns="label")

            return templates.TemplateResponse("generator.html", {
                "request":     request, 
                "name":         username,
                "languages":    languages,
                "platforms":    platforms,
                "models":       models,
                }
            )
    return templateInfoMessage("Вы не авторизованы!", request)


# Обработчик GET-запросов, апи генератора
@generator_router.get("/emb_code_gen", response_class=HTMLResponse)
async def generate_code(
        request: Request, 
        language: str, platform: str, 
        task: str, model: str,
    ) -> HTMLResponse:
    '''
    Обработчик GET-запросов, апи генератора
    '''
    if request.cookies.get("session_id"):
        isAuth, role, username = auth.checkAuth(request.cookies.get("session_id"))
        if isAuth and role == "user":
            llm = LLmFactory.getLlm(model=model)
            audit = Audit()
            audit.add_record(username=username, record="Generation: " + language + " " + platform + " " + task)
            
            try:
                html_content = llm.generateCodeLog(language=language,
                                                platform=platform,
                                                task=task,
                                                retriever=request.state.retriever)
                prometheus_generate_metric.inc()
            except ModelError:
                return templateInfoMessage("Ошибка модели!", request)

            return HTMLResponse(content=html_content, 
                                status_code=200)