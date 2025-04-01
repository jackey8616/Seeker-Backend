from typing import Optional

from models import MongoDocument
from models.user.execution_count import ModelExecutionCount
from services.google.oauth.dtos.google_credentials import GoogleCredentials
from services.google.oauth.dtos.google_user_info import GoogleUserInfo


class ModelUser(MongoDocument):
    google_userinfo: GoogleUserInfo
    google_credentials: Optional[GoogleCredentials] = None
    execution_count: Optional[ModelExecutionCount] = None
