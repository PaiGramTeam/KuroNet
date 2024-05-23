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
    }.get(recognize_game_uid_first_digit(player_id, Game.MC))

    if server:
        return server

    raise ValueError(f"Player id {player_id} isn't associated with any server")


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
