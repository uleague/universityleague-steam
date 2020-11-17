from aiohttp import web
import logging
import sys
import asyncio
import random

from .uleague import ULeagueClient

from steam.errors import HTTPException
from steam.protobufs import EMsg, MsgProto
from steam.enums import EResult
from steam import WSForbidden, WSException

LOG = logging.getLogger(__name__)


class MainHandler:
    def __init__(self, loop, steam_bot):
        self.loop = loop
        self.steam_bot = steam_bot

    async def index(self, request):
        try:
            name = self.steam_bot.user.name
        except Exception as e:
            LOG.exception("Error occured")
            response = {"Error occured": e.args[0]}
            return web.json_response(
                response, status=500, content_type="application/json"
            )
        else:
            if name:
                body = {"Hello from": name}
                return web.json_response(
                    body, status=200, content_type="application/json"
                )


class FriendsHandler:
    _payload = ["steam_id"]

    def __init__(self, loop, steam_bot):
        self.loop = loop
        self.steam_bot = steam_bot

    async def get_friends(self, request):
        try:
            friends = self.steam_bot.user.friends
            response = [friend.id64 for friend in friends]
        except Exception as e:
            LOG.exception("Error occured")
            response = {"Error occured": e.args[0]}
            return web.json_response(
                response, status=500, content_type="application/json"
            )
        else:
            return web.json_response(
                {"friends_steam_ids": response},
                status=200,
                content_type="application/json",
            )

    async def manual_friends_retry(self, new_friend):
        msg = MsgProto(EMsg.ClientAddFriend, steamid_to_add=new_friend.id64)
        await self.steam_bot.ws.send_as_proto(msg)
        try:
            coro = self.steam_bot.ws.wait_for(
                EMsg.ClientAddFriendResponse,
                lambda msg: msg.body.steam_id_added == new_friend.id64,
            )  # might be .id64 haven't checked
            msg = await asyncio.wait_for(coro, timeout=5)
        except asyncio.TimeoutError:
            # took too long to send
            LOG.exception("Took too long to send friend request")
        else:
            if msg.header.eresult == EResult.LimitExceeded:
                raise WSForbidden(msg)
            if msg.eresult != EResult.OK:
                raise WSException(msg)

    async def post_friends(self, request):
        try:
            body = await request.json()
            steam_id = body["steam_id"]
            new_friend = await self.steam_bot.fetch_user(steam_id)
            LOG.info(
                "Adding a friend {}. Steam id: {}".format(new_friend.name, steam_id)
            )
            if new_friend not in self.steam_bot.user.friends:
                if len(self.steam_bot.user.friends) > 150:
                    LOG.info("Deleting friends cause reaching 150 friends")
                    for i in range(10):
                        f = random.choice(self.steam_bot.user.friends)
                        await f.remove()
                        i += 1
                await new_friend.add()
            else:
                LOG.info("{} is already in friend list".format(steam_id))
                uleague = ULeagueClient()
                try:
                    LOG.info("Requesting pending invite messages.")
                    messages = await uleague.get_invitation_message(steam_id)
                except Exception as e:
                    LOG.exception("Error happened")
                    raise e
                else:
                    for message in messages:
                        LOG.info("Sending message: {} to {}".format(message, steam_id))
                        await new_friend.send(message)
        except KeyError as e:
            LOG.exception("Error occured")
            response = {"Error occured": e.args[0]}
            return web.json_response(
                response, status=400, content_type="application/json"
            )
        except HTTPException as e:
            LOG.exception(
                "HTTP Steam error. Trying adding friend with manual proto msg"
            )
            if e.code == 400:
                await self.manual_friends_retry(new_friend)
        except Exception as e:
            LOG.exception("Error occured")
            response = {"Error occured": e.args[0]}
            return web.json_response(
                response, status=500, content_type="application/json"
            )
        else:
            resp = {
                "steam_id": new_friend.id64,
                "avatar": new_friend.avatar_url,
                "name": new_friend.name,
            }
            return web.json_response(resp, status=200, content_type="application/json")


class MessageHandler:
    def __init__(self, loop, steam_bot):
        self.loop = loop
        self.steam_bot = steam_bot

    async def post_message(self, request):
        try:
            body = await request.json()
            steam_id, message = body["steam_id"], body["message"]
            user = await self.steam_bot.fetch_user(steam_id)
            LOG.info(
                "Sending a message to {}. Steam id: {}".format(user.name, steam_id)
            )
            await user.send(message)
        except KeyError as e:
            LOG.exception("Error occured")
            response = {"Error occured": e.args[0]}
            return web.json_response(
                response, status=400, content_type="application/json"
            )
        except Exception as e:
            LOG.exception("Error occured")
            response = {"Error occured": e.args[0]}
            return web.json_response(
                response, status=500, content_type="application/json"
            )
        else:
            response = {"Success": "200"}
            return web.json_response(
                response, status=200, content_type="application/json"
            )
