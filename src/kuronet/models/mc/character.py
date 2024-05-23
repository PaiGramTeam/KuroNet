from kuronet.models.base import APIModel


class MCRole(APIModel):
    """MC Role."""

    roleId: int
    level: int
    roleName: str
    roleIconUrl: str
    rolePicUrl: str
    starLevel: int
    attributeId: int
    attributeName: str
    weaponTypeId: int
    weaponTypeName: str
    acronym: str
