from typing import List

from kuronet.models.base import APIModel


class MCExplorerAreaItem(APIModel):
    """Area item info list item."""

    type: int
    name: str
    progress: int


class MCExplorerAreaInfo(APIModel):
    """Area info list item."""

    areaId: int
    areaName: str
    areaProgress: int
    itemList: List[MCExplorerAreaItem]


class MCExplorerCountry(APIModel):
    """Country info list item."""

    countryId: int
    countryName: str
    detailPageFontColor: str
    detailPagePic: str
    detailPageProgressColor: str
    homePageIcon: str


class MCExplorerArea(APIModel):
    """Area info list item."""

    areaInfoList: List[MCExplorerAreaInfo]
    country: MCExplorerCountry
    countryProgress: str


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
        exploreList: List of area info.
        detectionInfoList: List of detection info.
        open: Open status.
    """

    detectionInfoList: List[MCExplorerDetection]
    exploreList: List[MCExplorerArea]
    open: bool
