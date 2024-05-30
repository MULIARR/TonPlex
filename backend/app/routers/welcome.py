from fastapi import APIRouter, Request
from starlette.templating import Jinja2Templates

from backend.app.config import app_config

welcome_router = APIRouter()

templates = Jinja2Templates(directory=app_config.TEMPLATES_DIR)


@welcome_router.get("/")
async def get_welcome(request: Request):
    return templates.TemplateResponse(
        "welcome.html",
        {
            "request": request
        }
    )
