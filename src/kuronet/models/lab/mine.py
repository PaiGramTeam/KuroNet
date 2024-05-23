from typing import Optional

from pydantic import BaseModel


class Mine(BaseModel):
    collectCount: int
    commentCount: int
    fansCount: int
    fansNewCount: int
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
