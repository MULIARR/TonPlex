from fastapi import APIRouter

wallet_setup_router = APIRouter(
    prefix="/wallet_setup"
)


@wallet_setup_router.get("")
async def get_wallet_setup():
    ...
