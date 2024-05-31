from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from backend.constants import WebApp


def create_start_app_markup() -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()

    markup.row(
        InlineKeyboardButton(
            text="Launch App",
            web_app=WebAppInfo(url=WebApp.ROOT_URL.value)
        )
    )

    return markup.as_markup()
