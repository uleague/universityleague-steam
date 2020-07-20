import os
import logging
import logging.handlers
import sys

from steam.ext import commands

from settings import *

bot = commands.Bot(command_prefix="!")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        bot.load_extension("cogs.{name}".format(name=filename[:-3]))

bot.run(STEAM_LOGIN, STEAM_PASSWORD, STEAM_API, shared_secret=STEAM_SHARED_SECRET)
