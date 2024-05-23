from typing import TYPE_CHECKING

import pytest
import pytest_asyncio

from kuronet.client.components.lab import LabClient

if TYPE_CHECKING:
    from kuronet.client.cookies import Cookies
    from kuronet.utils.enums import Region


@pytest_asyncio.fixture
async def client_instance(account_id: int, region: "Region", cookies: "Cookies"):
    async with LabClient(
        cookies=cookies,
        account_id=account_id,
        region=region,
    ) as client_instance:
        yield client_instance


@pytest.mark.asyncio
class TestLabClient:
    @staticmethod
    async def test_find_event_list(client_instance: "LabClient"):
        event_list = await client_instance.find_event_list()
        assert event_list

    @staticmethod
    async def test_get_user_info(account_id: int, client_instance: "LabClient"):
        user_info = await client_instance.verify_token()
        assert user_info.userName
        assert int(user_info.userId) == account_id
