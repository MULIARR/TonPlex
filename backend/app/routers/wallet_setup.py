from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from backend.config import config

templates = Jinja2Templates(directory=config.app.TEMPLATES_DIR)

wallet_setup_router = APIRouter(
    prefix="/wallet_setup"
)


@wallet_setup_router.get("/create")
async def get_wallet_setup(request: Request):

    # TODO: create wallet with tontools
    wallet_mnemonics = [
        "apple", "bread", "clock", "dance", "eagle", "flame",
        "grape", "house", "index", "jumps", "kites", "lemon",
        "mango", "night", "olive", "plant", "queen", "river",
        "sunny", "trees", "under", "vivid", "wings", "zebra"
    ]

    return templates.TemplateResponse(
        "create_wallet.html",
        {
            "wallet_mnemonic_phrase": wallet_mnemonics,
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
