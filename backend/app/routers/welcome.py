from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from backend.config import config

templates = Jinja2Templates(directory=config.app.TEMPLATES_DIR)

welcome_router = APIRouter()


@welcome_router.get("/")
async def get_welcome(request: Request):
    return templates.TemplateResponse(
        "welcome.html",
        {
            "request": request
        }
    )
