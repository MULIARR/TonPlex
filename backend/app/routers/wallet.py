from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from backend.classes.ton_api_client import tonapi
from backend.classes.ton_wallet_manager import ton_wallet_manager
from backend.config import config
from backend.database.repo.user import user_repo

templates = Jinja2Templates(directory=config.app.TEMPLATES_DIR)

wallet_router = APIRouter(
    prefix="/wallet"
)


@wallet_router.get("/")
async def wallet(request: Request, user_id: int):
    # get user
    user_model = await user_repo.get_user(user_id)

    # get user's wallet
    wallet_model = ton_wallet_manager.get_wallet(user_model.mnemonic)

    # get wallet data
    wallet_data = await tonapi.get_wallet_assets_data(wallet_model)

    # get wallet transactions
    transactions_data = await tonapi.get_transactions(wallet_model.address)

    return templates.TemplateResponse(
        "wallet.html",
        {
            "request": request,
            "wallet_data": wallet_data,
            "transactions_data": transactions_data
        }
    )
