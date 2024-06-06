from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from backend.classes.ton_wallet_manager import ton_manager
from backend.config import config
from backend.database.repo.user import user_repo

templates = Jinja2Templates(directory=config.app.TEMPLATES_DIR)

wallet_setup_router = APIRouter(
    prefix="/wallet"
)


@wallet_setup_router.post("/")
async def get_wallet_setup(request: Request, user_model: UserModel):

    print(user_model)

    # create TON wallet (Oh no that sync!!!)
    wallet_model = ton_manager.create_wallet()

    # db entry
    # await user_repo.create_user()

    return templates.TemplateResponse(
        "wallet_created.html",
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
