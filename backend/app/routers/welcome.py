from fastapi import APIRouter, Request
from starlette.templating import Jinja2Templates

from backend.config import config

welcome_router = APIRouter()

templates = Jinja2Templates(directory=config.app.TEMPLATES_DIR)


@welcome_router.get("/")
async def get_welcome(request: Request):
    return templates.TemplateResponse(
        "welcome.html",
        {
            "request": request
        }
    )
