from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from backend.config import config

templates = Jinja2Templates(directory=config.app.TEMPLATES_DIR)


wallet_setup_router = APIRouter(
    prefix="/wallet_setup"
)


@wallet_setup_router.get("")
async def get_wallet_setup(request: Request):

    return templates.TemplateResponse(
        "welcome.html",
        {
            "request": request
        }
    )
