from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import html

import config
from modules.database import Generations

class Llm:
    def generate_code(self, language: str, platform: str, task: str, model: str) -> str:
        # Настраиваем LLM-модель Ollama
        llm = ChatOllama(model=model, temperature=0, base_url=config.LLM_BASE_URL)
        generations = Generations()

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

        generations.add_generation(task=task,
                                   code=response)

        return html_content