from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from backend.bot.filters.private_chat import IsPrivateChatFilter
from backend.bot.keyboards.start import create_start_app_markup
from backend.constants import Photo

starting_router = Router()


@starting_router.message(CommandStart(), IsPrivateChatFilter())
async def start(
        message: Message,
        bot: Bot,
        state: FSMContext
):
    user_id = message.from_user.id

    # clear state
    await state.clear()

    await bot.send_photo(
        chat_id=user_id,
        photo=Photo.START,
        reply_markup=create_start_app_markup()
    )
