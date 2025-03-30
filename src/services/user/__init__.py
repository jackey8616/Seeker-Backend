from dataclasses import dataclass, field
from typing import Optional

from models.user import ModelUser
from repository.user import UserRepository
from services.google.oauth.dtos.google_credentials import GoogleCredentials
from services.google.oauth.dtos.google_user_info import GoogleUserInfo


@dataclass
class UserService:
    _user_repository: UserRepository = field(default_factory=lambda: UserRepository())

    def get_by_id(self, user_id: str) -> Optional[ModelUser]:
        return self._user_repository.get_by_id(id=user_id)

    def get_by_google_id(self, google_id: str) -> Optional[ModelUser]:
        return self._user_repository.get_by_google_id(google_id=google_id)

    def create_new_user_through_oauth(
        self, userinfo: GoogleUserInfo, credentials: GoogleCredentials
    ) -> ModelUser:
        return self._user_repository.insert_one(
            obj=ModelUser(
                google_userinfo=userinfo,
                google_credentials=credentials,
            )
        )

    def update(self, user: ModelUser):
        self._user_repository.update(user=user)
