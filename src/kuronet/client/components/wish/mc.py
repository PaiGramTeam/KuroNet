from typing import Optional, List

from kuronet.client.components.wish.base import BaseWishClient
from kuronet.errors import BadRequest, InvalidAuthkey
from kuronet.models.mc.wish import MCWish, MCBannerType
from kuronet.utils.enums import Game

__all__ = ("MCWishClient",)

from kuronet.utils.player import recognize_mc_server


class MCWishClient(BaseWishClient):
    """The MCWishClient class for making requests towards the Wish API."""

    @staticmethod
    def fix_wish_item_id(data: List[MCWish]) -> List[MCWish]:
        temp = {}
        now_time_stamp = 0
        for i in data:
            if i.time.timestamp() != now_time_stamp:
                now_time_stamp = i.time.timestamp()
                temp.clear()
            if i.item_id not in temp:
                temp[i.item_id] = 1
            else:
                temp[i.item_id] += 1
            item_id = "{:08}".format(i.item_id)
            i.id = int(f"{int(i.time.timestamp())}{item_id}{temp[i.item_id]}")
        return data

    async def wish_history(
        self,
        record_id: str,
        banner_types: Optional[List[int]] = None,
        player_id: Optional[int] = None,
        lang: Optional[str] = "zh-Hans",
    ) -> List[MCWish]:
        """
        Get the wish history for a list of banner types.

        Args:
            record_id (str): The record ID to get the wish history for.
            banner_types (Optional[List[int]], optional): The banner types to get the wish history for.
                Defaults to None.
            player_id (Optional[int], optional): The player ID to get the wish history for.
                Defaults to None.
            lang (Optional[str], optional): The language code to use for the request.
                Defaults to None.

        Returns:
            List[StarRailWish]: A list of StarRailWish objects representing the retrieved wishes.
        """
        banner_types = banner_types or [1, 2, 3, 4, 5, 6, 7]
        if isinstance(banner_types, int):
            banner_types = [banner_types]
        wishes = []
        path = "gacha/record/query"
        player_id = player_id or self.player_id
        server_id = recognize_mc_server(player_id)
        data_ = {
            "playerId": str(player_id),
            "cardPoolId": "917dfa695d6c6634ee4e972bb9168f6a",
            "serverId": server_id,
            "recordId": record_id,
        }
        for banner_type in banner_types:
            data_["cardPoolType"] = banner_type
            banner_type_ = MCBannerType(banner_type)
            try:
                items = await self.request_gacha_info(path, Game.MC, data=data_, lang=lang)
            except BadRequest:
                raise InvalidAuthkey
            wishes.extend([MCWish(**i, banner_type=banner_type_) for i in items])
        temp_data = sorted(wishes, key=lambda wish: wish.time.timestamp())
        return self.fix_wish_item_id(temp_data)
