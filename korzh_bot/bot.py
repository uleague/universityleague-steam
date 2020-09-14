"""
=====
This module initializes the steam client by calling Bot class.
=====

Registering all cogs from /cogs directory for interacting with the bot in
the chat. Might be useful in the future.

It also registers the main events which are neccessary for the korzh_bot.
Contains following events. Bot listens for them and reacts accordingly.:
    * on_ready
        ..note::
            Basically is used only for senging log message that everything is fine.
    * on_socket_receive
        ..note::
            Is used to detect all messages from the Steam Coordinator.
            Within it messages are filtered to only detect new friend event.
"""

from steam.ext.commands import Bot
from steam.protobufs.steammessages_clientserver_friends import CMsgClientFriendsList

from typing import Literal, Awaitable
import os
import logging

from .uleague import ULeagueClient
from .cogs.basic import Basic

LOG = logging.getLogger(__name__)

steam_bot = Bot(command_prefix="!")
steam_bot.add_cog(Basic(steam_bot))


@steam_bot.event
async def on_ready() -> None:
    """
    Logging for checking if logging is successful
    """
    LOG.info("------------")
    LOG.info("Logged in as")
    LOG.info("Username: {}".format(steam_bot.user))
    LOG.info("ID: {}".format(steam_bot.user.id64))
    LOG.info("Friends: {}".format(len(steam_bot.user.friends)))
    LOG.info("------------")


@steam_bot.event
async def on_socket_receive(msg) -> None:
    """
    Receives every message from Steam Coordinator.
    .. note::
        We have to mannualy determine the event. Since lib doesn' t have on_new_friend.
        Calls ULeague API to get necessary message for the new friend.
        Then sends it.

    :param msg: Proto message from Steam Coordinator
    """
    if isinstance(msg.body, CMsgClientFriendsList):
        if (
            len(msg.body.friends) == 1
        ):  # check if the incoming proto msg is a single friend request
            friend: CMsgClientFriendsList = msg.body.friends[0]
            friend_steam_id, friend_relations = (
                friend.ulfriendid,
                friend.efriendrelationship,
            )
            if friend_relations == 3:  # acceptance scenario
                # make a request to backend
                uleague = ULeagueClient()
                try:
                    messages = await uleague.get_invitation_message(friend_steam_id)
                except Exception:
                    LOG.exception("Error happened")
                    raise
                else:
                    new_friend = await steam_bot.fetch_user(friend_steam_id)
                    for message in messages:
                        LOG.info(
                            "Sending message: {} to {}".format(message, friend_steam_id)
                        )
                        await new_friend.send(message)
