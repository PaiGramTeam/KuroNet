from typing import Optional

from kuronet.models.base import APIModel, Field


class Account(APIModel):
    userId: int
    gameId: int
    server: str = Field(alias="serverId")
    server_name: str = Field(alias="serverName")
    uid: int = Field(alias="roleId")
    level: int = Field(alias="gameLevel")
    nickname: str = Field(alias="roleName")
    isDefault: bool
    gameHeadUrl: Optional[str] = None
    roleNum: int
    fashionCollectionPercent: float
    phantomPercent: float
    achievementCount: int
    actionRecoverSwitch: bool
