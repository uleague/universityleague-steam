import os
import sys
from asyncio import get_event_loop

from steam.ext.commands import Bot
from api import routes

from asyncio import gather, get_event_loop
from logger import get_logger

from aiohttp.web import AppRunner, Application, TCPSite
from sys import argv

LOG = get_logger("Main")

from settings import STEAM_LOGIN, STEAM_PASSWORD, STEAM_API, STEAM_SHARED_SECRET


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
        LOG.info("Starting the bot...")
        await bot.start(
            STEAM_LOGIN, STEAM_PASSWORD, STEAM_API, shared_secret=STEAM_SHARED_SECRET
        )
        LOG.info("-" * 30)
        LOG.info("Logged in as: {}".format(bot.user.name))
        LOG.info("URL: {}".format(bot.user.community_url))
        LOG.info("-" * 30)
    except:
        LOG.exception()
        await bot.close(),
        raise
    finally:
        await runner.cleanup()


if __name__ == "__main__":
    loop = get_event_loop()
    loop.run_until_complete(run_bot())
