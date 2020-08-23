import asyncio
import pytest
from unittest import mock

from . import FakeSteam
from korzh_bot.handlers import MainHandler


async def test_index_sucess(cli, loop):
    "Get health check"
    resp = await cli.get("/")
    result = await resp.json()
    assert resp.status == 200
    assert {"Hello from": "ULeague"} == result


async def test_get_friends_success(cli, loop):
    "Get friends list"
    resp = await cli.get("/friends")
    result = await resp.json()
    assert resp.status == 200
    assert "friends_steam_ids" in result
    assert isinstance(result["friends_steam_ids"], list)


async def test_post_friends_success(cli, loop):
    "Add a friend with right data"
    data = {"steam_id": 12345678}
    resp = await cli.post("/friends", json=data)
    result = await resp.json()
    assert resp.status == 200
    assert "steam_id" in result
    assert "avatar" in result
    assert "name" in result


async def test_post_friends_fail(cli, loop):
    "Add a friend with right data"
    data = {"steamid": 12345678}
    resp = await cli.post("/friends", json=data)
    assert resp.status == 400


async def test_post_message_success(cli, loop):
    "Send a message"
    data = {"steam_id": 12345678, "message": "Hello!"}
    resp = await cli.post("/message", json=data)
    result = await resp.json()
    assert resp.status == 200
    assert {"Success": "200"} == result
