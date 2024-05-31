import asyncio
import logging

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
from backend.config import Config, config


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

        # await db.create_pool(**vars(config.db))
        await dp.start_polling(bot)
    finally:
        # await db.pool.close()
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
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


async def main(config: Config):
    setup_logging()

    app_task = asyncio.create_task(start_app())
    bot_task = asyncio.create_task(start_bot(config))

    await asyncio.gather(app_task, )

    # uvicorn.run(app, port=8000)  # host="0.0.0.0"


if __name__ == "__main__":
    asyncio.run(main(config))
