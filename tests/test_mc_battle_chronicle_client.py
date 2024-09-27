from typing import TYPE_CHECKING

import pytest
import pytest_asyncio

from kuronet.client.components.chronicle.mc import MCBattleChronicleClient
from kuronet.utils.enums import Game

if TYPE_CHECKING:
    from kuronet.client.cookies import Cookies
    from kuronet.utils.enums import Region


@pytest_asyncio.fixture
async def mc_client(
    mc_player_id: int, account_id: int, region: "Region", cookies: "Cookies"
):
    if mc_player_id is None:
        pytest.skip("Test case test_mc skipped: No mc player id set.")
    async with MCBattleChronicleClient(
        player_id=mc_player_id,
        cookies=cookies,
        account_id=account_id,
        region=region,
    ) as client_instance:
        client_instance.game = Game.MC
        yield client_instance


@pytest.mark.asyncio
class TestMCBattleChronicleClient:
    @staticmethod
    async def test_refresh_data(mc_client: "MCBattleChronicleClient"):
        assert await mc_client.refresh_data()

    @staticmethod
    async def test_get_mc_notes(mc_client: "MCBattleChronicleClient"):
        notes = await mc_client.get_mc_notes(auto_refresh=False)
        assert notes

    @staticmethod
    async def test_get_mc_notes_widget(mc_client: "MCBattleChronicleClient"):
        notes = await mc_client.get_mc_notes_widget(auto_refresh=False)
        assert notes

    @staticmethod
    async def test_get_mc_explorer(mc_client: "MCBattleChronicleClient"):
        explorer = await mc_client.get_mc_explorer(auto_refresh=False)
        assert explorer

    @staticmethod
    async def test_get_mc_roles(mc_client: "MCBattleChronicleClient"):
        roles = await mc_client.get_mc_roles(auto_refresh=False)
        assert roles

    @staticmethod
    async def test_get_mc_calabash(mc_client: "MCBattleChronicleClient"):
        calabash = await mc_client.get_mc_calabash(auto_refresh=False)
        assert calabash

    @staticmethod
    async def test_get_mc_role_detail(mc_client: "MCBattleChronicleClient"):
        role = await mc_client.get_mc_role_detail(role_id=1204, auto_refresh=False)
        assert role

    @staticmethod
    @pytest.mark.xfail
    async def test_get_mc_role_detail_failed(mc_client: "MCBattleChronicleClient"):
        await mc_client.get_mc_role_detail(role_id=1000, auto_refresh=False)
