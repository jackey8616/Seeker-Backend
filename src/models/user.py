from typing import Optional

from pydantic import BaseModel, Field

from dtos.google.credentials import GoogleCredentials
from dtos.google.userinfo import GoogleUserInfo
from utils.typings import PyObjectId


class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    google_userinfo: GoogleUserInfo
    google_credentials: GoogleCredentials
