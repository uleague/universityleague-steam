from steam.ext.commands import Bot

import logging

LOG = logging.getLogger(__name__)

steam_bot = Bot(command_prefix="!")


@steam_bot.event
async def on_ready():
    LOG.info("------------")
    LOG.info("Logged in as")
    LOG.info("Username: {}".format(bot.user))
    LOG.info("ID: {}".format(bot.user.id64))
    LOG.info("Friends: {}".format(len(bot.user.friends)))
    LOG.info("------------")


@steam_bot.event
async def on_user_invite(invite):
    invitee = invite.invitee
    LOG.info(
        "Got invite from {}. Steam URL: {}. Steam id: {}".format(
            invitee.name, invitee.community_url, invitee.id64
        )
    )
