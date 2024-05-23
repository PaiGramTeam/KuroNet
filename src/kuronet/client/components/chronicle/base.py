from typing import Optional, Any

from kuronet.client.base import BaseClient
from kuronet.client.routes import BBS_URL
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
    ):
        """Make a request towards the game record endpoint.

        Args:
            endpoint (str): The endpoint to send the request to.
            endpoint_type (str, optional): The type of endpoint to send the request to.
            data (Optional[Any], optional): The request payload.
            params (Optional[QueryParamTypes], optional): The query parameters for the request.
            lang (Optional[str], optional): The language for the response.
            region (Optional[Region], optional): The region associated with the request.

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

        return await self.request_lab(url, data=data, params=params, lang=lang)

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
        game = game or self.game
        player_id = player_id or self.player_id
        server_id = recognize_server(player_id, game)
        path = "aki/refreshData"
        data = {
            "gameId": game.game_id,
            "roleId": player_id,
            "serverId": server_id,
        }
        return await self.request_game_record(path, data=data)
