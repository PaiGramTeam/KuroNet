import enum as _enum

__all__ = ("Region", "Game")


class Region(str, _enum.Enum):
    """
    Represents a region where a game is being played.

    Attributes:
        OVERSEAS (Region): Represents an overseas region where a game is being played.
        CHINESE (Region): Represents a Chinese region where a game is being played.
    """

    OVERSEAS = "os"
    CHINESE = "cn"


class Game(str, _enum.Enum):
    """
    Represents a game that can be played in different regions.

    Attributes:
        MC (Game): Represents the game "Wuthering Waves".
    """

    MC = "G152"
