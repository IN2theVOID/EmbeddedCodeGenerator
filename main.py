import uvicorn
import config
from modules.controller import controller

# Запуск сервера Uvicorn
if __name__ == "__main__":
    uvicorn.run(controller, host="localhost", port=config.WEB_PORT)