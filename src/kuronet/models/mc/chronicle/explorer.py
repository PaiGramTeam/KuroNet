from typing import List

from kuronet.models.base import APIModel


class MCExplorerAreaItem(APIModel):
    """Area item info list item."""

    type: int
    name: str
    progress: int


class MCExplorerArea(APIModel):
    """Area info list item."""

    areaId: int
    areaProgress: int
    areaName: str
    itemList: List[MCExplorerAreaItem]


class MCExplorerDetection(APIModel):
    """Detection info list item."""

    detectionId: int
    detectionName: str
    detectionIcon: str
    level: int
    levelName: str
    acronym: str


class MCExplorer(APIModel):
    """MC Explorer.

    Attributes:
        countryCode: Country code.
        countryName: Country name.
        countryProgress: Country progress.
        areaInfoList: List of area info.
        detectionInfoList: List of detection info.
        open: Open status.
    """

    countryCode: int
    countryName: str
    countryProgress: float
    areaInfoList: List[MCExplorerArea]
    detectionInfoList: List[MCExplorerDetection]
    open: bool
