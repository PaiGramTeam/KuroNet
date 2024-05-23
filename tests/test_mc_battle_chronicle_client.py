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
        yield client_instance


@pytest.mark.asyncio
class TestMCBattleChronicleClient:
    @staticmethod
    async def test_refresh_data(mc_client: "MCBattleChronicleClient"):
        assert await mc_client.refresh_data(game=Game.MC)
