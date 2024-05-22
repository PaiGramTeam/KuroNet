"""This module contains functions for recognizing servers associated with different player IDs."""

from typing import Mapping, Sequence

from kuronet.utils.enums import Game, Region

UID_LENGTH: Mapping[Game, int] = {
    Game.MC: 9,
}
UID_RANGE: Mapping[Game, Mapping[Region, Sequence[int]]] = {
    Game.MC: {
        Region.OVERSEAS: (6, 7, 8, 18, 9),
        Region.CHINESE: (1, 2, 5),
    },
}
