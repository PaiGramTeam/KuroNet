from typing import List, Optional

from kuronet.models.base import APIModel
from kuronet.models.mc.character import MCRole


class MCRoles(APIModel):
    """MC Roles"""

    roleList: List[MCRole]
    showToGuest: bool


class MCRoleChain(APIModel):
    """Chain list item."""

    name: str
    order: int
    description: str
    iconUrl: str
    unlocked: bool


class MCRoleWeaponDetail(APIModel):
    """Role weapon detail."""

    weaponId: int
    weaponName: str
    weaponType: int
    weaponStarLevel: int
    weaponIcon: str
    weaponEffectName: str
    effectDescription: str


class MCRoleWeaponData(APIModel):
    """Role weapon data."""

    weapon: MCRoleWeaponDetail
    level: int
    resonLevel: int


class MCRolePhantomPhantomProp(APIModel):
    """Role phantom prop."""

    phantomPropId: int
    name: str
    phantomId: int
    quality: int
    cost: int
    iconUrl: str
    skillDescription: str


class MCRolePhantomFetterDetail(APIModel):
    """Role phantom fetter detail."""

    groupId: int
    name: str
    iconUrl: str
    num: int
    firstDescription: str
    secondDescription: str


class MCRolePhantomDetail(APIModel):
    """Role phantom detail."""

    phantomProp: MCRolePhantomPhantomProp
    cost: int
    quality: int
    level: int
    fetterDetail: MCRolePhantomFetterDetail


class MCRolePhantomData(APIModel):
    """Role phantom data."""

    cost: int
    equipPhantomList: Optional[List[Optional[MCRolePhantomDetail]]] = None


class MCRoleSkillDetail(APIModel):
    """Role skill detail."""

    id: int
    type: str
    name: str
    description: str
    iconUrl: str


class MCRoleSkill(APIModel):
    """Role skill item."""

    skill: MCRoleSkillDetail
    level: int


class MCRoleDetail(APIModel):
    """Role detail.

    Attributes:
        role: Role.
        level: Level.
        chainList: List of chain.
        weaponData: Weapon data.
        phantomData: Phantom data.
        skillList: List of skill.
    """

    role: MCRole
    level: int
    chainList: List[MCRoleChain]
    weaponData: MCRoleWeaponData
    phantomData: MCRolePhantomData
    skillList: List[MCRoleSkill]
