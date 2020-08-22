import asyncio
import pytest


@pytest.fixture
async def sleep_for_steam(loop):
    return await asyncio.sleep(25)


async def test_index(cli, loop, sleep_for_steam):
    resp = await cli.get("/")
    result = await resp.json()
    assert {"Hello from": "ULeague"} == result
