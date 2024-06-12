from fastapi import APIRouter

from .wallet import wallet_router
from .wallet_setup import wallet_setup_router

api_router = APIRouter(
    prefix="/api"
)

api_routers_tuple = (
    wallet_router,
    wallet_setup_router
)

for router in api_routers_tuple:
    api_router.include_router(router)

__all__ = [
    "api_router"
]
