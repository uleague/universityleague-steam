from aiohttp.web import RouteTableDef, json_response

routes = RouteTableDef()


@routes.get("/")
async def get_ping(request):
    client = request.app["bot"]
    response = {"I'm": client.user.name}
    return json_response(response, status=200, content_type="application/json")
