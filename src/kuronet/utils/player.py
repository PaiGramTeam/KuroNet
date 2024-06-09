"""This module contains functions for recognizing servers associated with different player IDs."""

from typing import Mapping, Sequence, Optional

from kuronet.utils.enums import Game, Region

UID_LENGTH: Mapping[Game, int] = {
    Game.MC: 9,
}
UID_RANGE: Mapping[Game, Mapping[Region, Sequence[int]]] = {
    Game.MC: {
        Region.OVERSEAS: (5, 6, 7, 8, 9),
        Region.CHINESE: (1, 2, 3, 4),
    },
}


def recognize_game_uid_first_digit(player_id: int, game: Game) -> int:
    """
    Recognizes the first digit of a game UID for a given game.

    Args:
        player_id (int): The player ID to recognize the first digit for.
        game (Game): The game the player ID belongs to.

    Returns:
        int: The first digit of the player ID.

    Raises:
        ValueError: If the specified uid is not right.
    """
    length = UID_LENGTH[game] - 1
    first = int(player_id / (10**length))
    if not first:
        raise ValueError(f"player id {player_id} is not right")
    return first


def recognize_mc_server(player_id: int) -> str:
    """Recognize which server a MC UID is from.

    Args:
        player_id (int): The player ID to recognize the server for.

    Returns:
        str: The name of the server associated with the given player ID.

    Raises:
        ValueError: If the player ID is not associated with any server.
    """
    server = {
        1: "76402e5b20be2c39f095a152090afddc",
        5: "591d6af3a3090d8ea00d8f86cf6d7501",  # America
        6: "6eb2a235b30d05efd77bedb5cf60999e",  # Europe
        7: "86d52186155b148b5c138ceb41be9650",  # Asia
        8: "919752ae5ea09c1ced910dd668a63ffb",  # HMT
        9: "10cd7254d57e58ae560b15d51e34b4c8",  # SEA
    }.get(recognize_game_uid_first_digit(player_id, Game.MC))

    if server:
        return server

    raise ValueError(f"Player id {player_id} isn't associated with any server")


def recognize_region(player_id: int, game: Game) -> Optional[Region]:
    """
    Recognizes the region of a player ID for a given game.

    Args:
        player_id (int): The player ID to recognize the region for.
        game (Game): The game the player ID belongs to.

    Returns:
        Optional[Region]: The region the player ID belongs to if it can be recognized, None otherwise.
    """
    for region, digits in UID_RANGE[game].items():
        first = recognize_game_uid_first_digit(player_id, game)
        if first in digits:
            return region

    return None


def recognize_server(player_id: int, game: Game) -> str:
    """
    Recognizes the server of a player ID for a given game.

    Args:
        player_id (int): The player ID to recognize the server for.
        game (Game): The game the player ID belongs to.

    Returns:
        str: The server the player ID belongs to.

    Raises:
        ValueError: If the specified game is not supported.
    """
    if game == Game.MC:
        return recognize_mc_server(player_id)
    raise ValueError(f"{game} is not a valid game")
