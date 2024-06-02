from pprint import pprint

from aiogram import Router, F
from aiogram.types import Message

web_app_data_router = Router()


@web_app_data_router.message(F.web_app_data)
async def handle_web_app_data(message: Message):
    pprint(message, indent=4, width=2)

    web_app_data = message.web_app_data.data

    await message.answer(f"Получены данные из веб-приложения: {web_app_data}")
