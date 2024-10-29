from typing import Optional

from kuronet.client.components.chronicle.base import BaseChronicleClient
from kuronet.errors import AccountNotFound
from kuronet.models.mc.chronicle.calabash import MCCalabash
from kuronet.models.mc.chronicle.explorer import MCExplorer
from kuronet.models.mc.chronicle.notes import MCNote, MCNoteWidget

__all__ = ("MCBattleChronicleClient",)

from kuronet.models.mc.chronicle.role import MCRoles, MCRoleDetail


class MCBattleChronicleClient(BaseChronicleClient):
    async def get_mc_notes(
        self,
        player_id: Optional[int] = None,
        lang: Optional[str] = None,
        auto_refresh: bool = True,
    ) -> MCNote:
        """Get the MC notes for the player.

        Args:
            player_id (Optional[int], optional): The player id to get the notes for. Defaults to None.
            lang (Optional[str], optional): The language code to use for the request. Defaults to None.
            auto_refresh (bool, optional): Whether to refresh the data before making the request. Defaults to True.

        Returns:
            MCNote: The MC notes for the player.
        """
        if auto_refresh:
            await self.refresh_data(player_id)
        path = "akiBox/baseData"
        data = await self.request_game_record(
            path, player_id=player_id, lang=lang, need_decrypt=True
        )
        if player_id and data is None:
            raise AccountNotFound
        return MCNote(**data)

    async def get_mc_notes_widget(
        self,
        player_id: Optional[int] = None,
        lang: Optional[str] = None,
        auto_refresh: bool = True,
    ) -> MCNoteWidget:
        """Get the MC notes widget for the player.

        Args:
            player_id (Optional[int], optional): The player id to get the notes widget for. Defaults to None.
            lang (Optional[str], optional): The language code to use for the request. Defaults to None.
            auto_refresh (bool, optional): Whether to refresh the data before making the request. Defaults to True.

        Returns:
            MCNoteWidget: The MC notes widget for the player.
        """
        path = "game3/getData"
        if auto_refresh:
            path = "game3/refresh"
        data_ = {
            "type": "2",
            "sizeType": "1",
        }
        data = await self.request_game_record(
            path,
            endpoint_type="widget",
            player_id=player_id,
            lang=lang,
            data=data_,
        )
        return MCNoteWidget(**data)

    async def get_mc_explorer(
        self,
        player_id: Optional[int] = None,
        country_code: Optional[int] = 1,
        lang: Optional[str] = None,
        auto_refresh: bool = True,
    ) -> MCExplorer:
        """Get the MC explorer for the player.

        Args:
            player_id (Optional[int], optional): The player id to get the explorer for. Defaults to None.
            country_code (Optional[int], optional): The country code to use for the request. Defaults to 1.
            lang (Optional[str], optional): The language code to use for the request. Defaults to None.
            auto_refresh (bool, optional): Whether to refresh the data before making the request. Defaults to True.

        Returns:
            MCExplorer: The MC explorer for the player.
        """
        if auto_refresh:
            await self.refresh_data(player_id)
        path = "akiBox/exploreIndex"
        data_ = {
            "channelId": "19",
            "countryCode": str(country_code),
        }
        data = await self.request_game_record(
            path,
            player_id=player_id,
            lang=lang,
            data=data_,
            need_decrypt=True,
        )
        return MCExplorer(**data)

    async def get_mc_roles(
        self,
        player_id: Optional[int] = None,
        lang: Optional[str] = None,
        auto_refresh: bool = True,
    ) -> MCRoles:
        """Get the MC roles for the player.

        Args:
            player_id (Optional[int], optional): The player id to get the roles for. Defaults to None.
            lang (Optional[str], optional): The language code to use for the request. Defaults to None.
            auto_refresh (bool, optional): Whether to refresh the data before making the request. Defaults to True.

        Returns:
            MCRoles: The MC roles for the player.
        """
        if auto_refresh:
            await self.refresh_data(player_id)
        path = "akiBox/roleData"
        data = await self.request_game_record(
            path,
            player_id=player_id,
            lang=lang,
            need_decrypt=True,
        )
        return MCRoles(**data)

    async def get_mc_calabash(
        self,
        player_id: Optional[int] = None,
        lang: Optional[str] = None,
        auto_refresh: bool = True,
    ) -> MCCalabash:
        """Get the MC calabash for the player.

        Args:
            player_id (Optional[int], optional): The player id to get the calabash for. Defaults to None.
            lang (Optional[str], optional): The language code to use for the request. Defaults to None.
            auto_refresh (bool, optional): Whether to refresh the data before making the request. Defaults to True.

        Returns:
            MCCalabash: The MC calabash for the player.
        """
        if auto_refresh:
            await self.refresh_data(player_id)
        path = "akiBox/calabashData"
        data = await self.request_game_record(
            path,
            player_id=player_id,
            lang=lang,
            need_decrypt=True,
        )
        return MCCalabash(**data)

    async def get_mc_role_detail(
        self,
        player_id: Optional[int] = None,
        role_id: Optional[int] = None,
        lang: Optional[str] = None,
        auto_refresh: bool = True,
    ) -> MCRoleDetail:
        """Get the MC role detail for the player.

        Args:
            player_id (Optional[int], optional): The player id to get the role detail for. Defaults to None.
            role_id (Optional[int], optional): The role id to get the role detail for. Defaults to None.
            lang (Optional[str], optional): The language code to use for the request. Defaults to None.
            auto_refresh (bool, optional): Whether to refresh the data before making the request. Defaults to True.

        Returns:
            MCRoleDetail: The MC role detail for the player.
        """
        if auto_refresh:
            await self.refresh_data(player_id)
        path = "akiBox/getRoleDetail"
        data_ = {
            "channelId": "19",
            "countryCode": "1",
            "id": role_id,
        }
        data = await self.request_game_record(
            path,
            player_id=player_id,
            lang=lang,
            data=data_,
            need_decrypt=True,
        )
        if data.get("level") is None:
            raise ValueError("Role not found.")
        return MCRoleDetail(**data)
