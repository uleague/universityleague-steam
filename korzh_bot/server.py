import asyncio

from aiohttp import web

from .bot import steam_bot
from .settings import Config, SteamConfig
from .handlers import MainHandler
from .router import setup_index_handler
from .utils.logger import setup_logging
import logging

LOG = logging.getLogger("Main")


def setup_cleanup_hooks(tasks):
    async def cleanup(app):
        for func in tasks:
            result = func()
            if asyncio.iscoroutine(result):
                result = await result

    return cleanup


async def bot_start(app):
    bot = steam_bot
    try:
        await bot.start(
            SteamConfig.LOGIN,
            SteamConfig.PASSWORD,
            shared_secret=SteamConfig.SHARED_SECRET,
        )
    except:
        raise
    finally:
        await bot.close()


def setup_startup_hooks(loop):
    async def startup(app):
        app["background_bot"] = asyncio.create_task(bot_start(app))

    return startup


async def init_application(loop):
    app = web.Application()

    handler = MainHandler(loop, steam_bot)

    setup_index_handler(app, handler)

    app.on_startup.append(setup_startup_hooks(loop))

    app.on_cleanup.append(setup_cleanup_hooks([steam_bot.close,]))

    return app


def main():
    setup_logging()
    loop = asyncio.get_event_loop()
    app = init_application(loop)
    web.run_app(app, host="localhost", port=Config.PORT)
