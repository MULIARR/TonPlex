from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from backend.app.models.user import UserModel
from backend.classes.ton_wallet_manager import ton_manager
from backend.config import config
from backend.database.repo.user import user_repo

templates = Jinja2Templates(directory=config.app.TEMPLATES_DIR)

wallet_router = APIRouter(
    prefix="/wallet"
)


@wallet_router.get("/")
async def get_wallet(request: Request, user_id: int):
    # print(user_model)
    #
    # # create TON wallet (Oh no that sync!!!)
    # wallet_model = ton_manager.create_wallet()
    #
    # # db entry
    # # await user_repo.create_user()

    wallet_data = {
        "balance": 90.97,
        "address": "Uia78HFjnjwe892JIJEi_GSybq8",
        "shorten_address": "Uia78...GSybq8",
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
