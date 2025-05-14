from typing import List, Optional

from kuronet.models.base import APIModel, Field, DateTimeField


class MCNoteDataEntryModel(APIModel):
    """Represents a battle pass data entry in a MCNote."""

    name: str
    img: Optional[str] = ""
    refreshTimeStamp: Optional[DateTimeField] = None
    timePreDesc: Optional[str] = None
    expireTimeStamp: Optional[DateTimeField] = None
    status: int
    cur: int
    total: int


class MCNoteWidget(APIModel):
    """Represents a MCNote widget.

    Attributes:
        gameId (int): The ID of the game.
        account_id (int): The ID of the account.
        serverTime (datetime): The server time.
        serverId (str): The ID of the server.
        serverName (str): The name of the server.
        hasSignIn (bool): Indicates whether the account has signed in.
        uid (int): The ID of the role.
        nickname (str): The nickname of the role.
        energyData (EnergyData): The energy data.
        livenessData (LivenessData): The liveness data.
        battlePassData (List[MCNoteBattlePassDatum]): The battle pass data.
    """

    gameId: int
    account_id: int = Field(alias="userId")

    serverTime: DateTimeField
    serverId: str
    serverName: str

    hasSignIn: bool

    uid: int = Field(alias="roleId")
    nickname: str = Field(alias="roleName")

    energyData: MCNoteDataEntryModel
    livenessData: Optional[MCNoteDataEntryModel]
    battlePassData: List[Optional[MCNoteDataEntryModel]]
    storeEnergyData: Optional[MCNoteDataEntryModel]
    towerData: Optional[MCNoteDataEntryModel]
    slashTowerData: Optional[MCNoteDataEntryModel]
    weeklyData: Optional[MCNoteDataEntryModel]

    @property
    def current_stamina(self) -> int:
        """The current stamina of the role."""
        return self.energyData.cur

    @property
    def max_stamina(self) -> int:
        """The maximum stamina of the role."""
        return self.energyData.total

    @property
    def current_liveness(self) -> int:
        """The current liveness of the role."""
        return self.livenessData.cur if self.livenessData else 0

    @property
    def max_liveness(self) -> int:
        """The maximum liveness of the role."""
        return self.livenessData.total if self.livenessData else 0


class MCNoteBoxListItem(APIModel):
    """Represents a MCNote box list item."""

    boxName: str
    num: int


class MCNoteBoxListItem2(APIModel):
    """Represents a MCNote box list item."""

    name: str
    num: int


class MCNote(APIModel):
    """Represents a MCNote.

    Attributes:
        nickname (str): The nickname of the role.
        uid (int): The ID of the role.
        creatTime (datetime): The creation time of the role.
        activeDays (int): The number of active days.
        level (int): The level of the role.
        worldLevel (int): The world level of the role.
        roleNum (int): The role number.
        soundBox (int): The sound box.
        current_stamina (int): The current stamina of the role.
        max_stamina (int): The maximum stamina of the role.
        current_liveness (int): The current liveness of the role.
        max_liveness (int): The maximum liveness of the role.
        livenessUnlock (bool): Indicates whether the liveness is unlocked.
        chapterId (int): The ID of the chapter.
        bigCount (int): The big count.
        smallCount (int): The small count.
        achievementCount (int): The achievement count.
        boxList (List[MCNoteBoxListItem]): A list of box list items.
        showToGuest (bool): Indicates whether the role is shown to guests.
    """

    nickname: str = Field(alias="name")
    uid: int = Field(alias="id")
    creatTime: DateTimeField
    activeDays: int
    level: int
    worldLevel: int
    roleNum: int

    current_stamina: int = Field(alias="energy")
    max_stamina: int = Field(alias="maxEnergy")

    rougeScore: int
    rougeScoreLimit: int
    rougeIconUrl: str
    rougeTitle: str

    storeEnergy: int
    storeEnergyLimit: int
    storeEnergyIconUrl: str
    storeEnergyTitle: str

    weeklyInstCount: int
    weeklyInstCountLimit: int
    weeklyInstIconUrl: str
    weeklyInstTitle: str

    current_liveness: int = Field(alias="liveness")
    max_liveness: int = Field(alias="livenessMaxCount")
    livenessUnlock: bool

    chapterId: int

    bigCount: int
    smallCount: int
    achievementCount: int
    achievementStar: int
    boxList: List[MCNoteBoxListItem]
    phantomBoxList: List[MCNoteBoxListItem2]
    treasureBoxList: List[MCNoteBoxListItem2]
    showToGuest: bool
