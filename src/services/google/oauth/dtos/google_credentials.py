from datetime import datetime

from pydantic import BaseModel


class GoogleCredentials(BaseModel):
    token: str
    refresh_token: str
    expiry: datetime
