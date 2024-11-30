from enum import IntEnum
from typing import Optional

from kuronet.models.base import APIModel, Field, DateTimeField


class MCBannerType(IntEnum):
    """Banner types in wish histories."""

    CHARACTER = 1
    """Rotating character banner."""

    WEAPON = 2
    """Rotating weapon banner."""

    STANDARD = 3
    """standard banner."""
    STANDARD_WEAPON = 4
    """standard banner."""

    TEMPORARY = 5
    """Temporary banner."""
    TEMPORARY_SELF = 6
    """Temporary banner."""
    TEMPORARY_GIFT = 7
    """Temporary banner."""


class MCWish(APIModel, frozen=False):
    """Wish made on any banner."""

    id: Optional[int] = 0
    """ID of the wished item."""

    type: str = Field(alias="resourceType")
    """Type of the wished item."""

    item_id: int = Field(alias="resourceId")
    """ID of the wished item."""

    name: str
    """Name of the wished item."""

    rarity: int = Field(alias="qualityLevel")
    """Rarity of the wished item."""

    count: int
    """Count of the wished item."""

    time: DateTimeField
    """Time when the wish was made."""

    banner_name: str = Field(alias="cardPoolType")
    """Name of the banner the wish was made on."""

    banner_type: Optional[MCBannerType] = None
    """Type of the banner the wish was made on."""
