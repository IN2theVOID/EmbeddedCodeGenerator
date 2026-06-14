import logging

class ECDLogger:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
    
    def info(self, message: str) -> None:
        logging.info(message)

    def error(self, message: str) -> None:
        logging.error(message)

log = ECDLogger()
