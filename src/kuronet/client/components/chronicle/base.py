import datetime
from typing import Optional, Any

from kuronet.client.base import BaseClient
from kuronet.client.routes import BBS_URL
from kuronet.models.lab.daily import DailyRewardInfo
from kuronet.utils.enums import Region, Game
from kuronet.utils.player import recognize_server
from kuronet.utils.types import QueryParamTypes

__all__ = ("BaseChronicleClient",)


class BaseChronicleClient(BaseClient):
    """The base class for the Chronicle API client.

    This class provides the basic functionality for making requests to the
    Chronicle API endpoints. It is meant to be subclassed by other clients
    that provide a more specific interface to the Chronicle API.

    Attributes:
        region (Region): The region associated with the API client.
    """

    async def request_game_record(
        self,
        endpoint: str,
        endpoint_type: str = "roleBox",
        data: Optional[Any] = None,
        params: Optional[QueryParamTypes] = None,
        lang: Optional[str] = None,
        region: Optional[Region] = None,
        player_id: Optional[int] = None,
        game: Optional[Game] = None,
        need_decrypt: bool = False,
    ):
        """Make a request towards the game record endpoint.

        Args:
            endpoint (str): The endpoint to send the request to.
            endpoint_type (str, optional): The type of endpoint to send the request to.
            data (Optional[Any], optional): The request payload.
            params (Optional[QueryParamTypes], optional): The query parameters for the request.
            lang (Optional[str], optional): The language for the response.
            region (Optional[Region], optional): The region associated with the request.
            player_id (Optional[int], optional): The player id associated with the request.
            game (Optional[Game], optional): The game associated with the request.
            need_decrypt (bool, optional): Whether the response needs to be decrypted.

        Returns:
            The response from the server.

        Raises:
            NetworkError: If an HTTP error occurs while making the request.
            TimedOut: If the request times out.
            BadRequest: If the response contains an error.
        """
        base_url = BBS_URL.get_url(region or self.region)
        base_url = base_url / "gamer" / endpoint_type
        url = base_url / endpoint

        game = game or self.game
        player_id = player_id or self.player_id
        server_id = recognize_server(player_id, game)
        base_data = {
            "gameId": game.game_id,
            "roleId": player_id,
            "serverId": server_id,
        }
        data = {**base_data, **data} if data else base_data

        return await self.request_lab(
            url, data=data, params=params, lang=lang, need_decrypt=need_decrypt
        )

    async def refresh_data(
        self,
        player_id: Optional[int] = None,
        *,
        game: Optional[Game] = None,
    ) -> bool:
        """Refresh the data for the player.

        Args:
            player_id (Optional[int], optional): The player id to refresh the data for.
            game (Optional[Game], optional): The game associated with the player.

        Returns:
            bool: True if the data was refreshed successfully.
        """
        path = "akiBox/refreshData"
        return await self.request_game_record(path, player_id=player_id, game=game)

    async def get_reward_info(
        self,
        *,
        lang: Optional[str] = None,
    ) -> DailyRewardInfo:
        """Gets the daily reward info for the current user.

        Args:
            lang (str): The language to use. Defaults to None.

        Returns:
            A DailyRewardInfo object containing information about the user's daily reward status.
        """
        path = "../../encourage/signIn/initSignInV2"
        _data = {
            "userId": self.account_id,
        }
        data = await self.request_game_record(path, lang=lang, data=_data)
        return DailyRewardInfo(**data)

    async def claim_daily_reward(
        self,
        *,
        lang: Optional[str] = None,
    ) -> bool:
        path = "../../encourage/signIn/v2"
        month = datetime.datetime.now().month
        req_month = f"{month:02d}"
        _data = {
            "userId": self.account_id,
            "reqMonth": req_month,
        }
        return await self.request_game_record(path, lang=lang, data=_data)
