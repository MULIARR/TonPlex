from .wallet_setup import wallet_setup_router
from .welcome import welcome_router

routers_tuple = (
    wallet_setup_router,
    welcome_router
)

__all__ = [
    "routers_tuple"
]