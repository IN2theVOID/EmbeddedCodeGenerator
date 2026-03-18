from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
import uvicorn
import html  # Для безопасного экранирования HTML

from modules.static import static_form
import config

# Создаем контроллер API
controller = FastAPI()

# Настраиваем LLM-модель Ollama
llm = ChatOllama(model=config.LLM_MODEL, temperature=0, base_url=config.LLM_BASE_URL)

@controller.get("/")
def emb_code_gen_form() -> HTMLResponse:
    html_content = static_form
    return HTMLResponse(content=html_content, status_code=200)

# Обработчик GET-запросов
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