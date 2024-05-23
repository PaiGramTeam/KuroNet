from typing import Optional, Dict, Any

from kuronet.client.base import BaseClient
from kuronet.client.headers import Headers
from kuronet.client.routes import BBS_URL
from kuronet.models.lab.mine import Mine
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
            },
        )
        return data

    async def verify_token(
        self, user_token: Optional[str] = None, account_id: Optional[int] = None
    ) -> Optional[Mine]:
        """
        Retrieves a super ticket (`stoken`) using a login ticket (`login_ticket`) .

        Args:
            user_token (Optional[str]): The login ticket to use to retrieve the super ticket. If not provided, the
                `user_token` cookie value will be used.
            account_id (Optional[int]): The account ID to use to retrieve the super ticket. If not provided, the
                `account_id` attribute value will be used.

        Returns:
            Optional[Mine]: The user.

        Raises:
            ValueError: If `user_token` or `account_id` is not provided.
            InvalidCookies: If the user_token is invalid.
        """
        path = "user/mineV2"
        user_token = user_token or self.user_token
        account_id = account_id or self.account_id
        if user_token is None:
            raise ValueError("The 'user_token' argument cannot be None.")
        if account_id is None:
            raise ValueError("The 'account_id' argument cannot be None.")
        data = {
            "otherUserId": str(account_id),
        }
        headers = {
            "token": user_token,
        }
        data = await self.request_bbs(path, data=data, headers=headers)
        return Mine(**data.get("mine", {}))
