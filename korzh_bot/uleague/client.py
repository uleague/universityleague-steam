import aiohttp
from typing import List, Text

from .exceptions import ULeagueRequestError

from korzh_bot.settings import Config

import logging

LOG = logging.getLogger(__name__)


class ULeagueClient:
    """
    Class for interacting with ULeague API.

    ...

    Attributes
    ----------
    URL: str
        backend url
    TOKEN: str
        token

    Methods
    ----------
    get_invitation_message(steam_id:int)
        gets invitation messages.
    """

    URL: str = Config.BACKEND_URL
    TOKEN: str = Config.BACKEND_TOKEN

    async def get_invitation_message(self, steam_id: int) -> List[Text]:
        """
        Get the invitation messages for a requested user.

        >>> await ULeagueAPI.get_invitation_message(123456)

        :param steam_id: Steam id64 for the desired user.
        :type steam_id: int
        :returns: list of messages for the user
        :rtype: List[Text]
        """
        _URL = "{}/api/v1/users/{}/invitations".format(self.URL, steam_id)
        body = {"token": self.TOKEN}
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(_URL, json=body) as r:
                    resp = await r.json()
        except (aiohttp.ClientResponseError, aiohttp.ClientConnectorError):
            raise
        else:
            if "error" in resp:
                LOG.error("Error occured {}".format(resp["errors"]))
                raise ULeagueRequestError("Error occured {}".format(resp["errors"]))
            else:
                return resp["messages"]
