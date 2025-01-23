from typing import Optional

from kuronet.models.base import APIModel


class Mine(APIModel):
    collectCount: int
    commentCount: int
    fansCount: int
    followCount: int
    gender: int
    goldNum: int
    headUrl: str
    ipRegion: str
    isFollow: int
    isLoginUser: int
    isMute: int
    lastLoginModelType: Optional[str] = ""
    lastLoginTime: Optional[str] = ""
    levelTotal: int
    likeCount: int
    postCount: int
    registerTime: str
    signature: str
    signatureReviewStatus: int
    status: int
    userId: int
    userName: str
