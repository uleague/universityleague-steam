from aiohttp import web


class MainHandler:
    def __init__(self, loop, steam_bot):
        self.loop = loop
        self.steam_bot = steam_bot

    async def index(self, request):
        body = {"Hello from": self.steam_bot.user.name}
        return web.json_response(body, status=200, content_type="application/json")
