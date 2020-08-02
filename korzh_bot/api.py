from aiohttp.web import RouteTableDef, json_response
import logging

LOG = logging.getLogger(__name__)

routes = RouteTableDef()


@routes.get("/")
async def get_ping(request):
    """
    Heartbeat index route
    """
    client = request.app["bot"]
    response = {"I'm": client.user.name}
    return json_response(response, status=200, content_type="application/json")


@routes.get("/friends")
async def all_friends(request):
    """
    GET /friends
    Returns a list of friends' steamid
    """
    client = request.app["bot"]
    try:
        friends = client.user.friends
        response = [friend.id64 for friend in friends]
    except Exception as e:
        LOG.exception("Error occured")
        response = {"Error occured": e.args[0]}
        return json_response(response, status=500, content_type="application/json")
    else:
        return json_response(
            {"friends_steam_ids": response}, status=200, content_type="application/json"
        )


@routes.post("/friends")
async def add_friend(request):
    """
    PUT /friends {'steamid': 12345678}
    Adds a user to friends. Returns minimal info about user
    """
    client = request.app["bot"]
    try:
        body = await request.json()
        LOG.info(body)
        steam_id = body["steam_id"]
        new_friend = await client.fetch_user(steam_id)
        LOG.info("Adding a friend {}. Steam id: {}".format(new_friend.name, steam_id))
        await new_friend.add()
    except Exception as e:
        LOG.exception("Error occured")
        response = {"Error occured": e.args[0]}
        return json_response(response, status=500, content_type="application/json")
    else:
        resp = {
            "steam_id": new_friend.id64,
            "avatar": new_friend.avatar_url,
            "name": new_friend.name,
        }
        return json_response(resp, status=200, content_type="application/json")
