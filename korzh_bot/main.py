import os
import sys
from asyncio import get_event_loop

from steam.ext.commands import Bot
from api import routes

from asyncio import gather, get_event_loop
from logging import basicConfig, INFO

from aiohttp.web import AppRunner, Application, TCPSite
from sys import argv


basicConfig(level=INFO)

from settings import *


async def run_bot():

    app = Application()
    app.add_routes(routes)

    runner = AppRunner(app)
    await runner.setup()
    site = TCPSite(runner, "0.0.0.0", 8080)
    await site.start()

    bot = Bot(command_prefix="!")

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            bot.load_extension("cogs.{name}".format(name=filename[:-3]))

    app["bot"] = bot

    try:
        await bot.start(
            STEAM_LOGIN, STEAM_PASSWORD, STEAM_API, shared_secret=STEAM_SHARED_SECRET
        )

    except:
        bot.close(),
        raise

    finally:
        await runner.cleanup()


if __name__ == "__main__":
    loop = get_event_loop()
    loop.run_until_complete(run_bot())
