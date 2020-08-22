from aiohttp import web
import logging

LOG = logging.getLogger(__name__)


class MainHandler:
    def __init__(self, loop, steam_bot):
        self.loop = loop
        self.steam_bot = steam_bot

    async def index(self, request):
        try:
            body = {"Hello from": self.steam_bot.user.name}
        except Exception as e:
            LOG.exception("Error occured")
            response = {"Error occured": e.args[0]}
            return web.json_response(
                response, status=500, content_type="application/json"
            )
        else:
            return web.json_response(body, status=200, content_type="application/json")


class FriendsHandler:
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

    async def post_friends(self, request):
        try:
            body = await request.json()
            steam_id = body["steam_id"]
            new_friend = await self.steam_bot.fetch_user(steam_id)
            LOG.info(
                "Adding a friend {}. Steam id: {}".format(new_friend.name, steam_id)
            )
            await new_friend.add()
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
