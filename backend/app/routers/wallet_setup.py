from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from backend.app.models.user import UserModel
from backend.classes.ton_wallet_manager import ton_wallet_manager
from backend.config import config
from backend.database.repo.user import user_repo

templates = Jinja2Templates(directory=config.app.TEMPLATES_DIR)

wallet_setup_router = APIRouter(
    prefix="/wallet_setup"
)


@wallet_setup_router.get("/import")
async def import_wallet(request: Request):
    return templates.TemplateResponse(
        "import_wallet.html",
        {
            "request": request
        }
    )


@wallet_setup_router.get("/created")
async def wallet_created(request: Request, user_id: int):
    # get user
    user_model = await user_repo.get_user(user_id)

    return templates.TemplateResponse(
        "wallet_created.html",
        {
            "request": request,
            "wallet_mnemonic_phrase": user_model.mnemonic
        }
    )
