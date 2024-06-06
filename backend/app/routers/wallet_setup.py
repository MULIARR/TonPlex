from pprint import pprint

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from backend.classes.ton_wallet_manager import ton_manager
from backend.config import config
from backend.database.repo.user import user_repo

templates = Jinja2Templates(directory=config.app.TEMPLATES_DIR)

wallet_setup_router = APIRouter(
    prefix="/wallet_setup"
)


@wallet_setup_router.get("/create")
async def get_wallet_setup(request: Request):

    # create TON wallet (Oh no that sync!!!)
    wallet_model = ton_manager.create_wallet()

    # db entry
    # await user_repo.create_user()

    return templates.TemplateResponse(
        "create_wallet.html",
        {
            "wallet_mnemonic_phrase": wallet_model.mnemonics,
            "request": request
        }
    )


@wallet_setup_router.get("/import")
async def get_wallet_setup(request: Request):
    return templates.TemplateResponse(
        "import_wallet.html",
        {
            "request": request
        }
    )
