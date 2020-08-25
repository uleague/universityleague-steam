# DEPRECATED

import os
import sys
from asyncio import get_event_loop

from bot import steam_bot
from api import routes

from asyncio import gather, get_event_loop
from .utils.logger import setup_logging
import logging

LOG = logging.getLogger("Main")

from aiohttp.web import AppRunner, Application, TCPSite

from .settings import Config, SteamConfig


async def run_bot():
    app = Application()
    app.add_routes(routes)

    runner = AppRunner(app)
    await runner.setup()
    site = TCPSite(runner, "0.0.0.0", Config.PORT)
    await site.start()

    bot = steam_bot

    app["bot"] = bot

    try:
        await bot.start(
            SteamConfig.STEAM_LOGIN,
            SteamConfig.STEAM_PASSWORD,
            SteamConfig.STEAM_API,
            shared_secret=SteamConfig.STEAM_SHARED_SECRET,
        )
    except:
        await bot.close(),
        raise
    finally:
        await runner.cleanup()


if __name__ == "__main__":
    # starting
    setup_logging()
    loop = get_event_loop()
    loop.run_until_complete(run_bot())
