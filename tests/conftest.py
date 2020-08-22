import pytest
import asyncio
from aiohttp import web
from korzh_bot.server import init_application


@pytest.fixture
async def app(loop, aiohttp_server):
    app = init_application(loop)
    return await aiohttp_server(app)


@pytest.fixture
async def cli(loop, aiohttp_client, app):
    return await aiohttp_client(app)
