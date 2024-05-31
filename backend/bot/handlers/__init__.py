from aiogram import Router

from .starting import starting_router

main_router = Router()

main_router.include_routers(
    starting_router
)

__all__ = [
    "main_router"
]
