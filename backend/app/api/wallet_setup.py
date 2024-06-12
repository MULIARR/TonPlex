from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse

from backend.app.models.mnemonics import MnemonicsModel
from backend.app.models.user import UserModel
from backend.classes.ton_wallet_manager import ton_wallet_manager
from backend.database.repo.user import user_repo

wallet_setup_router = APIRouter(
    prefix="/wallet_setup"
)


@wallet_setup_router.post("/create")
async def create_wallet(request: Request, user_model: UserModel):

    # create TON wallet (Oh no that sync!!!)
    wallet_model = ton_wallet_manager.create_wallet()

    # db entry
    await user_repo.create_user(
        user_model.id,
        wallet_model.mnemonics
    )

    return RedirectResponse(url=f"/wallet_setup/created?user_id={user_model.id}", status_code=303)


@wallet_setup_router.post("/check_mnemonics")
async def check_mnemonics(request: Request, mnemonics_model: MnemonicsModel):
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
