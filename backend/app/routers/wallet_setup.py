from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from backend.app.models.mnemonics import MnemonicsModel
from backend.app.models.user import UserModel
from backend.classes.ton_wallet_manager import ton_wallet_manager
from backend.config import config
from backend.database.repo.user import user_repo

templates = Jinja2Templates(directory=config.app.TEMPLATES_DIR)

wallet_setup_router = APIRouter(
    prefix="/wallet_setup"
)


@wallet_setup_router.post("/create")
async def get_wallet_setup(request: Request, user_model: UserModel):

    # create TON wallet (Oh no that sync!!!)
    wallet_model = ton_wallet_manager.create_wallet()

    # db entry
    await user_repo.create_user(
        user_model.id,
        wallet_model.mnemonics
    )

    return RedirectResponse(url=f"/wallet_setup/created?user_id={user_model.id}", status_code=303)


@wallet_setup_router.post("/check_mnemonics")
async def get_wallet_setup(request: Request, mnemonics_model: MnemonicsModel):
    # get TON wallet (Oh no that sync!!!)
    wallet_model = ton_wallet_manager.get_wallet(mnemonics=mnemonics_model.mnemonics)

    if wallet_model:
        # db entry
        await user_repo.create_user(
            mnemonics_model.user_id,
            wallet_model.mnemonics
        )

        return {"success": True}
    else:
        return {"success": False}


@wallet_setup_router.get("/import")
async def wallet_created(request: Request):
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
