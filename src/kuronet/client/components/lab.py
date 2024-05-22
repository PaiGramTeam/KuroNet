from typing import Optional, Dict, Any

from kuronet.client.base import BaseClient
from kuronet.client.headers import Headers
from kuronet.client.routes import BBS_URL
from kuronet.utils.enums import Region
from kuronet.utils.types import HeaderTypes

__all__ = ("LabClient",)


class LabClient(BaseClient):
    """LabClient component."""

    async def request_bbs(
        self,
        endpoint: str,
        *,
        lang: Optional[str] = None,
        region: Optional[Region] = None,
        method: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        data: Any = None,
        headers: Optional[HeaderTypes] = None,
    ) -> Dict[str, Any]:
        """Makes a request to a bbs endpoint.

        Args:
            endpoint (str): The URL of the endpoint to make the request to.
            lang (str, optional): The language code used for the request. Defaults to None.
            region (Region, optional): The server region used for the request. Defaults to None.
            method (str, optional): The HTTP method used for the request. Defaults to None.
            params (dict, optional): The parameters to include in the request. Defaults to None.
            data (any, optional): The data to include in the request. Defaults to None.
            headers (dict, optional): The headers to include in the request. Defaults to None.

        Returns:
            Dict[str, Any]: The response data from the request.
        """
        headers = Headers(headers)

        lang = lang or self.lang
        region = region or self.region

        url = BBS_URL.get_url(region) / endpoint

        data = await self.request_lab(
            url,
            method=method,
            params=params,
            data=data,
            headers=headers,
            lang=lang,
        )
        return data

    async def find_event_list(
            self,
            event_type: int = 1,
            game_id: int = 3,
            page_no: int = 1,
            page_size: int = 10,
    ):
        """Find a list of events.

        Args:
            event_type (int, optional): The type of event to find. Defaults to 1.
            game_id (int, optional): The ID of the game to find events for. Defaults to 3.
            page_no (int, optional): The page number to get. Defaults to 1.
            page_size (int, optional): The number of items to get per page. Defaults to 10.

        Returns:
            dict: The response data from the request."""
        data = await self.request_bbs(
            "forum/companyEvent/findEventList",
            data={
                "eventType": str(event_type),
                "gameId": str(game_id),
                "pageNo": str(page_no),
                "pageSize": str(page_size),
            }
        )
        return data
