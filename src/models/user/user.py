from typing import Optional

from dtos.google.oauth_dtos import GoogleCredentials, GoogleUserInfo
from models import MongoDocument
from models.user.execution_count import ModelExecutionCount


class ModelUser(MongoDocument):
    google_userinfo: GoogleUserInfo
    google_credentials: Optional[GoogleCredentials] = None
    execution_count: Optional[ModelExecutionCount] = None
