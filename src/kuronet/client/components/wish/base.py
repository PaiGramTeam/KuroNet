from typing import Optional, Any, List, Dict

from kuronet.client.base import BaseClient
from kuronet.client.routes import GACHA_INFO_URL
from kuronet.utils.enums import Game

__all__ = ("BaseWishClient",)


class BaseWishClient(BaseClient):
    """The base class for the Wish API client."""

    async def request_gacha_info(
        self,
        endpoint: str,
        game: Game,
        lang: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> List[Any]:
        """
        Make a request towards the gacha info endpoint.

        Args:
            endpoint (str): The endpoint to request data from.
            game (Game): The game to make the request for.
            lang (Optional[str] , optional): The language code to use for the request.
                If not provided, the class default will be used.
            data (Optional[Dict[str, Any]], optional): The query parameters for the request.

        Returns:
            Dict[str, Any]
                The response data as a dictionary.
        """

        base_url = GACHA_INFO_URL.get_url(self.region, game)
        url = base_url / endpoint

        if data and lang:
            data["languageCode"] = lang

        return await self.request_api("POST", url, json=data, accept_code=0)
