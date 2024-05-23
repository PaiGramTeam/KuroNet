from typing import Optional

from kuronet.client.components.chronicle.base import BaseChronicleClient
from kuronet.models.mc.chronicle.notes import MCNote, MCNoteWidget

__all__ = ("MCBattleChronicleClient",)


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
        path = "aki/baseData"
        data = await self.request_game_record(path, player_id=player_id, lang=lang)
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
        if auto_refresh:
            await self.refresh_data(player_id)
        path = "game3/getData"
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
