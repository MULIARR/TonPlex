from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse, HTMLResponse

from backend.config import config
from backend.database.repo.user import user_repo

templates = Jinja2Templates(directory=config.app.TEMPLATES_DIR)

welcome_router = APIRouter()


@welcome_router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )


@welcome_router.get("/redirect")
async def redirect_user(request: Request, user_id: int):

    user = await user_repo.get_user(user_id)

    if user:
        return RedirectResponse(url=f"/wallet?user_id={user_id}", status_code=303)

    return templates.TemplateResponse(
        "welcome.html",
        {
            "request": request
        }
    )
