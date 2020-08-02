from aiohttp.web import RouteTableDef, json_response
from logger import get_logger

LOG = get_logger(__name__)

routes = RouteTableDef()


@routes.get("/")
async def get_ping(request):
    client = request.app["bot"]
    response = {"I'm": client.user.name}
    return json_response(response, status=200, content_type="application/json")


@routes.put("/friends")
async def add_friend(request):
    """
    PUT /friends {'steamid': 12345678}
    """
    client = request.app["bot"]
    try:
        steamid = request.content.steamid
        new_friend = await client.fetch_user(steamid)
        LOG.info("Adding a friend {}. Steam id: {}".format(new_friend.name, steamid))
        await new_friend.add()
    except Exception as e:
        LOG.exception("Error occured")
        response = {"Error occured": e}
        return json_response(response, status=500, content_type="application/json")
    else:
        return json_response(
            {"Success": "200"}, status=200, content_type="application/json"
        )
