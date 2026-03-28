
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from fastapi.responses import HTMLResponse

from fastapi import FastAPI, Response, Cookie, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
import html

from modules.auth import Auth
from modules.database import Audit, Admin
import config

# Создаем контроллер API
controller = FastAPI()

templates = Jinja2Templates(directory="templates")

# Авторизация
auth = Auth()

# Настраиваем LLM-модель Ollama
llm = ChatOllama(model=config.LLM_MODEL, temperature=0, base_url=config.LLM_BASE_URL)

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
            admin = Admin()
            
            users = admin.get_records("users", "username")
            roles = admin.get_records("roles", "username, role")
            languages = admin.get_records("languages", "label")
            platforms = admin.get_records("platforms", "label")
            models = admin.get_records("models", "label")
            devices = admin.get_records("devices", "label,address")

            return templates.TemplateResponse("admin.html", {"request":         request, 
                                                                "name":         username,
                                                                "users":        users,
                                                                "roles":        roles,
                                                                "languages":    languages,
                                                                "platforms":    platforms,
                                                                "models":       models,
                                                                "devices":      devices})
    return {"message": "Вы не авторизованы!"}

# Консоль администратора
@controller.get("/dashboard")
def dashboard(request: Request) -> HTMLResponse:
    if request.cookies.get("session_id"):
        isAuth, role, username = auth.checkAuth(request.cookies.get("session_id"))
        if isAuth and role == "viewer":
            admin = Admin()
            
            languages = admin.get_records("languages", "label")
            platforms = admin.get_records("platforms", "label")
            models = admin.get_records("models", "label")
            devices = admin.get_records("devices", "label,address")
            generations = admin.get_records("generations", "prompt,code")

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
            return templates.TemplateResponse("generator.html", {"request":     request, 
                                                                "name":         username})
    return {"message": "Вы не авторизованы!"}

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
async def generate_code(request: Request, language: str, platform: str, task: str) -> HTMLResponse:
    if request.cookies.get("session_id"):
        isAuth, role, username = auth.checkAuth(request.cookies.get("session_id"))
        if isAuth and role == "user":
            # Формируем шаблон промта для модели
            prompt = ChatPromptTemplate.from_messages([
                ("system", "Ты - разработчик встаиваемых модулей на языке {language}.Платформа {platform}."),
                ("user", "Напиши код по задаче:{task}.В ответе только код, без комментариев.")
            ])
            
            audit = Audit()
            audit.add_record(username=username, record="Generation: " + language + " " + platform + " " + task)

            # Создаем цепочку обработчиков
            chain = prompt | llm | StrOutputParser()
            
            # Получаем ответ от модели
            response = chain.invoke({"language":language, 
                                    "platform":platform,
                                    "task":task})
            

            # Безопасно экранируем спецсимволы HTML и форматируем код
            escaped_response = html.escape(response)
            formatted_code = escaped_response.replace('\n', '<br>').replace('  ', '&nbsp;&nbsp;')
            
            # Формируем полноценный HTML-документ с базовым стилем
            html_content = f"""
            <!DOCTYPE html>
            <html lang="ru">
            <body>
                {formatted_code}
            </body>
            </html>
            """
            
            return HTMLResponse(content=html_content, status_code=200)