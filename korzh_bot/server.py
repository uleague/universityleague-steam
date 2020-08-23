import asyncio

from aiohttp import web

from .bot import steam_bot
from .settings import Config, SteamConfig
from .handlers import MainHandler, FriendsHandler, MessageHandler
from .router import setup_index_handler, setup_friends_handler, setup_message_handler
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
    try:
        await steam_bot.start(
            SteamConfig.LOGIN,
            SteamConfig.PASSWORD,
            shared_secret=SteamConfig.SHARED_SECRET,
        )
    except:
        raise
    finally:
        await steam_bot.close()


def setup_startup_hooks(loop):
    async def startup(app):
        app["background_bot"] = asyncio.create_task(bot_start(app))

    return startup


def init_application(loop):
    app = web.Application()

    handler = MainHandler(loop, steam_bot)
    friends_handler = FriendsHandler(loop, steam_bot)
    message_handler = MessageHandler(loop, steam_bot)

    setup_index_handler(app, handler)
    setup_friends_handler(app, friends_handler)
    setup_message_handler(app, message_handler)

    app.on_startup.append(setup_startup_hooks(loop))
    app.on_cleanup.append(setup_cleanup_hooks([steam_bot.close,]))

    return app


def main():
    setup_logging()
    loop = asyncio.get_event_loop()
    app = init_application(loop)
    web.run_app(app, host="0.0.0.0", port=Config.PORT)
