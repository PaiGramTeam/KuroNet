from typing import List, Optional

from kuronet.models.base import APIModel, Field


class DisposableGoodsListItem(APIModel):
    """Disposable goods list item."""

    goodsId: int
    name: str = Field(alias="goodsName")
    amount: int = Field(alias="goodsNum")
    icon: str = Field(alias="goodsUrl")
    isGain: bool
    serialNum: int


class SignInGoodsConfig(APIModel):
    """Sign-in goods configuration."""

    goodsId: int
    name: str = Field(alias="goodsName")
    amount: int = Field(alias="goodsNum")
    icon: str = Field(alias="goodsUrl")
    id: int
    isGain: bool
    serialNum: int
    signId: int


class DailyRewardInfo(APIModel):
    """Model for the daily reward info."""

    disposableGoodsList: Optional[List[DisposableGoodsListItem]] = None
    disposableSignNum: Optional[int] = 0
    eventEndTimes: str
    eventStartTimes: str
    expendGold: int
    expendNum: int
    signed_in: bool = Field(alias="isSigIn")
    nowServerTimes: str
    missed_rewards: int = Field(alias="omissionNnm")
    openNotifica: bool
    redirectContent: str
    redirectText: str
    redirectType: int
    repleNum: int
    claimed_rewards: int = Field(alias="sigInNum")
    signInGoodsConfigs: List[SignInGoodsConfig]
