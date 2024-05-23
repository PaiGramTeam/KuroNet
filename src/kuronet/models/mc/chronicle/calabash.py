from typing import List

from kuronet.models.base import APIModel


class MCCalabashPhantomItem(APIModel):
    """MC Calabash Phantom item."""

    name: str
    phantomId: int
    cost: int
    iconUrl: str
    acronym: str


class MCCalabashPhantom(APIModel):
    """MC Calabash Phantom."""

    phantom: MCCalabashPhantomItem
    star: int
    maxStar: int


class MCCalabash(APIModel):
    """MC Calabash.

    Attributes:
        level: Level.
        baseCatch: Base catch.
        strengthenCatch: Strengthen catch.
        catchQuality: Catch quality.
        cost: Cost.
        maxCount: Max count.
        unlockCount: Unlock count.
        phantomList: List of phantom.
    """

    level: int

    baseCatch: str
    strengthenCatch: str
    catchQuality: int
    cost: int

    phantomList: List[MCCalabashPhantom]
    maxCount: int
    unlockCount: int
