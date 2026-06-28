import logging
from typing import Callable

class ECDLogger:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
    
    def info(self, message: str) -> None:
        logging.info(message)

    def error(self, message: str) -> None:
        logging.error(message)

class LoggerDecorator:
    def __init__(self):
        self.logger = log
    
    def __call__(self, f) -> Callable:
        def wrapped(*args, **kwargs):
            self.logger.info(f"Execute: {f.__name__} with kwargs {kwargs} and args {args[1:]}")
            return f(*args, **kwargs)
        return wrapped

log = ECDLogger()
