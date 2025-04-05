from datetime import datetime

from pydantic import BaseModel


class GoogleCredentials(BaseModel):
    token: str
    refresh_token: str
    expiry: datetime


class GoogleUserInfo(BaseModel):
    id: str
    name: str
    family_name: str
    given_name: str
    picture: str
