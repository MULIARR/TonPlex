import asyncio
import logging
import os

import betterlogging as bl
import uvicorn
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.app.routers import routers_tuple
from backend.bot.handlers import main_router
from backend.bot.middlewares.config import ConfigMiddleware
from backend.classes.ton_wallet_manager import ton_wallet_manager
from backend.config import Config, config
from backend.database.db import database
from backend.utils.logo import print_logo


def get_storage(config):
    """
    Return storage based on the provided configuration.
    """
    if config.tg_bot.use_redis:
        ...
    else:
        return MemoryStorage()


def register_global_middlewares(dp: Dispatcher, config: Config):
    """
    Register global middlewares for the given dispatcher.
    Global middlewares here are the ones that are applied to all the handlers
    """
    middleware_types = [
        ConfigMiddleware(config),
    ]

    for middleware_type in middleware_types:
        dp.message.outer_middleware(middleware_type)
        dp.callback_query.outer_middleware(middleware_type)


def setup_logging():
    """
    Set up logging configuration for the application.
    """
    log_level = logging.INFO
    bl.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting App")


async def lazy_init():
    """
    An asynchronous function for lazily initializing clients or other objects.

    This function is needed to initialize objects that should only be created
    when accessing them for the first time, thereby postponing the creation of resource-intensive objects
    until they are actually needed.

    The function is called on a shared asynchronous event pool, ensuring that initialization occurs
    in an asynchronous context without blocking the main thread of execution.
    :return:
    """
    await ton_wallet_manager.init_client()

    await database.init_db()


async def start_bot(config: Config):
    try:
        # launch bot
        bot = Bot(
            token=config.tg_bot.token,
            default=DefaultBotProperties(
                parse_mode="HTML"
            )
        )

        storage = get_storage(config)
        dp = Dispatcher(storage=storage)
        dp.include_router(main_router)
        register_global_middlewares(dp, config)

        await bot.delete_webhook(drop_pending_updates=True)

        await dp.start_polling(bot)
    finally:
        ...


def create_app(config: Config) -> FastAPI:
    app = FastAPI()

    app.mount("/static", StaticFiles(directory=config.app.STATIC_DIR), name="static")

    for router in routers_tuple:
        app.include_router(router)

    return app


# Creating an application at the module level (to run the application locally)
#  -> uvicorn launcher:app --reload --port 8005
app = create_app(config)


async def start_app():
    port = int(os.environ.get("PORT", 8005))  # Railway port
    config = uvicorn.Config(app, host="0.0.0.0", port=port, log_level="info")
    server = uvicorn.Server(config)

    await server.serve()


async def main(config: Config):
    setup_logging()
    await lazy_init()

    app_task = asyncio.create_task(start_app())
    bot_task = asyncio.create_task(start_bot(config))

    await asyncio.gather(app_task, bot_task)


if __name__ == "__main__":
    print_logo()
    asyncio.run(main(config))
