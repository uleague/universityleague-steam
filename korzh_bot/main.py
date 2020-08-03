import os
import sys
from asyncio import get_event_loop

from bot import steam_bot
from api import routes

from asyncio import gather, get_event_loop
from logger import setup_logging
import logging

LOG = logging.getLogger("Main")

from aiohttp.web import AppRunner, Application, TCPSite
from sys import argv

from settings import STEAM_LOGIN, STEAM_PASSWORD, STEAM_API, STEAM_SHARED_SECRET, PORT


async def run_bot():
    app = Application()
    app.add_routes(routes)

    runner = AppRunner(app)
    await runner.setup()
    site = TCPSite(runner, "0.0.0.0", PORT)
    await site.start()

    bot = steam_bot

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            bot.load_extension("cogs.{name}".format(name=filename[:-3]))

    app["bot"] = bot

    try:
        await bot.start(
            STEAM_LOGIN, STEAM_PASSWORD, STEAM_API, shared_secret=STEAM_SHARED_SECRET
        )
    except:
        await bot.close(),
        raise
    finally:
        await runner.cleanup()


if __name__ == "__main__":
    setup_logging()
    loop = get_event_loop()
    loop.run_until_complete(run_bot())
