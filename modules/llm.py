from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import html

import config
from modules.database import Generations
from modules.exceptions import ModelError
from modules.logger import log

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

class LLmFactory():
    @staticmethod
    def getLlm(model) -> Llm:
        return Llm(model=model)

class Llm:
    def __init__(self, model) -> None:
        # Настраиваем LLM-модель Ollama
        self.llm = ChatOllama(model=model, temperature=0, base_url=config.LLM_BASE_URL)
        self.generations = Generations()

    def generateCodeLog(self, language: str, 
                        platform: str, 
                        task: str,
                        retriever) -> str:
        '''Декоратор с логированием'''
        log.info(f"Генерация. {language} {platform} {task}")
        return self.generateCode(language=language,
                                    platform=platform,
                                    task=task,
                                    retriever=retriever)

    def generateCode(self, language: str, 
                      platform: str, 
                      task: str,
                      retriever) -> str:
        # Формируем шаблон промта для модели
        generatePrompt = ChatPromptTemplate.from_messages([
            ("system", "Ты - разработчик встаиваемых модулей на языке {language}.Платформа {platform}.Документация: {context}"),
            ("user", "Напиши код по задаче:{task}.В ответе только код, без комментариев и эмодзи.")
        ])

        checkPrompt = ChatPromptTemplate.from_messages([
            ("system", "Ты - разработчик встаиваемых модулей на языке {language}.Платформа {platform}."),
            ("user", "Выполни проверку представленного кода на корректность, исправь и проведи рефакторинг, если считаешь нужным. В ответе только код, без комментариев и цепочки рассуждений. Код: {code}")
        ])
        
        # Создаем цепочку обработчиков
        chain = generatePrompt | self.llm | StrOutputParser()
        chainCheck = checkPrompt | self.llm | StrOutputParser()
        fullChain = chain | (lambda output: {"code": output, "language": language, "platform": platform}) | chainCheck

        try:
            # Получаем ответ от модели
            response = fullChain.invoke({"language":language, 
                                    "platform":platform,
                                    "task":task,
                                    "context":retriever | format_docs})
        except:
            raise ModelError()
        
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

        self.generations.add_generation(task=task,
                                   code=response)

        return html_content