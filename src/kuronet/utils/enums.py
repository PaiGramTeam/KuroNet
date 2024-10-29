import enum as _enum

__all__ = ("Region", "Game", "Platform")


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

    MC = "mc"

    @property
    def game_id(self):
        return {"mc": 3}[self.value]


class Platform(str, _enum.Enum):
    """
    Represents a platform where a game is being played.

    Attributes:
        H5 (Platform): Represents the H5 platform.
        ANDROID (Platform): Represents the Android platform.
        IOS (Platform): Represents the iOS platform.
    """

    H5 = "h5"
    ANDROID = "android"
    IOS = "ios"
