from typing import Optional

from kuronet.client.components.lab import LabClient
from kuronet.utils.enums import Game

__all__ = ("MCClient",)


class MCClient(
    LabClient,
):
    """A simple http client for mc endpoints."""

    game: Optional[Game] = Game.MC
