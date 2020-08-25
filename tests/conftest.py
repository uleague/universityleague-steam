import pytest
import asyncio
from aiohttp import web

from korzh_bot.handlers import MainHandler, FriendsHandler, MessageHandler
from korzh_bot.router import (
    setup_index_handler,
    setup_friends_handler,
    setup_message_handler,
)
from . import FakeSteam


@pytest.fixture
async def app(loop, aiohttp_server):
    app = web.Application()
    steam_bot = FakeSteam()

    handler = MainHandler(loop, steam_bot)
    friends_handler = FriendsHandler(loop, steam_bot)
    message_handler = MessageHandler(loop, steam_bot)

    setup_index_handler(app, handler)
    setup_friends_handler(app, friends_handler)
    setup_message_handler(app, message_handler)

    return app


@pytest.fixture
async def cli(loop, aiohttp_client, app):
    return await aiohttp_client(app)
