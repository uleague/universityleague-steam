from steam.ext.commands import Bot
from typing import Literal, Awaitable

from steam.protobufs.emsg import EMsg

import logging

LOG = logging.getLogger(__name__)

steam_bot = Bot(command_prefix="!")


@steam_bot.event
async def on_ready() -> None:
    LOG.info("------------")
    LOG.info("Logged in as")
    LOG.info("Username: {}".format(steam_bot.user))
    LOG.info("ID: {}".format(steam_bot.user.id64))
    LOG.info("Friends: {}".format(len(steam_bot.user.friends)))
    LOG.info("------------")


@steam_bot.event
async def on_socket_receive(msg) -> Awaitable[None]:
    """
    We have to mannualy determine the event. Since lib doesn't have on_new_friend
    """
