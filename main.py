from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from fastapi import FastAPI, Response, Cookie, Request, Form
from fastapi.responses import HTMLResponse
import uvicorn
import html
from typing import Annotated
from pydantic import BaseModel

import config
from modules.static import static_form, auth_form
from modules.auth import Auth, auth_tokens

# Создаем контроллер API
controller = FastAPI()

# Настраиваем LLM-модель Ollama
llm = ChatOllama(model=config.LLM_MODEL, temperature=0, base_url=config.LLM_BASE_URL)

# # AUTH Cookie
# @controller.get("/set-cookie")
# def create_cookie(response: Response):
    
#     response.set_cookie(key="session_id", value=Auth.authUser("user", "user"))
#     return {"message": "Cookie has been set"}

# @controller.get("/get-cookie")
# async def get_cookie(request: Request):
#     print(request.cookies.get("session_id"))
#     return request.cookies

@controller.post("/auth")
def auth_api(request: Request, response: Response, username: Annotated[str, Form()], password: Annotated[str, Form()]):
    '''
    Авторизация
    В случае успеха выдается session_id
    '''

    if request.cookies.get("session_id"):
        isAuth, role = Auth.checkAuth(request.cookies.get("session_id"))
        print(isAuth)
        if isAuth:
            return {"message": "Вы уже авторизованы", "role": role}
    
    authResponse = Auth.authUser(username, password)
    if authResponse.isAuth:
        response.set_cookie(key="session_id", value=authResponse.cookieString)
        return {"message": "Авторизация успешна", "auth_tokens": auth_tokens}
    else:
        return {"message": "Авторизация неуспешна"}

# Авторизация
@controller.get("/")
def auth_page() -> HTMLResponse:
    return HTMLResponse(content=auth_form, status_code=200)

# Генератор
@controller.get("/code_generator")
def emb_code_gen_form(request: Request) -> HTMLResponse:
    if request.cookies.get("session_id"):
        isAuth, role = Auth.checkAuth(request.cookies.get("session_id"))
        if isAuth:
            return HTMLResponse(content=static_form, status_code=200)
    return {"message": "Вы не авторизованы!"}

# Обработчик GET-запросов, апи генератора
@controller.get("/emb_code_gen", response_class=HTMLResponse)
async def simple_question(language: str, platform: str, task: str) -> HTMLResponse:
    # Формируем шаблон промта для модели
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Ты - разработчик встаиваемых модулей на языке {language}.Платформа {platform}."),
        ("user", "Напиши код по задаче:{task}.В ответе только код, без комментариев.")
    ])
    
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

# Запуск сервера Uvicorn
if __name__ == "__main__":
    uvicorn.run(controller, host="localhost", port=config.WEB_PORT)