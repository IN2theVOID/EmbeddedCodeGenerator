from fastapi import Request
from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse

templates = Jinja2Templates(directory="templates")

def templateInfoMessage(
        message: str, 
        request: Request,
    ) -> _TemplateResponse:
    return templates.TemplateResponse(
                    "message.html", {
                        "request": request, 
                        "message": message,
                        }
                )