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
async def get_wallet(request: Request, user_id: int):
    # # get user
    # user_model = await user_repo.get_user(user_id)
    #
    # # get user's wallet
    # wallet_model = ton_wallet_manager.get_wallet(user_model.mnemonics)
    #
    # # get wallet data
    # wallet_data = await tonapi.get_wallet_data(wallet_model.address)

    wallet_data = {
        "balance": 90.97,
        "address": "Uia78HFjnjwe892JIJEi_GSybq8",
        "shorten_address": "Uia78...GSybq8",
        "interface": "wallet_v4r2",
        "mnemonics": ['loyal', 'tiny', 'furnace', 'hip', 'such', 'curtain', 'ensure', 'fresh', 'rely', 'budget', 'rocket', 'system', 'suspect', 'confirm', 'hedgehog', 'okay', 'fuel', 'topic', 'force', 'spoon', 'stool', 'sunset', 'display', 'review'],
        "assets": {
            "TON": {
                "symbol": "TON",
                "name": "Toncoin",
                "value": 5,
                "price": 45.5,
                "img": None
            }
        }
    }

    return templates.TemplateResponse(
        "wallet.html",
        {
            "request": request,
            "wallet_data": wallet_data
        }
    )
