from dataclasses import dataclass, field
from typing import Optional

from dtos.auth.auth_dtos import Userinfo
from dtos.google.oauth_dtos import GoogleCredentials, GoogleUserInfo
from models.user.user import ModelUser
from repository.user import UserRepository
from services.quota.examinator.ai_quota import AiQuotaStrategyExaminator


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
        self._user_repository.update(obj=user)

    def get_user_info(self, user_id: str) -> Optional[Userinfo]:
        user = self._user_repository.get_by_id(id=user_id)
        if user is None:
            return None

        if user.execution_count is None:
            return Userinfo(
                name=user.google_userinfo.name,
                avatar_url=user.google_userinfo.picture,
                execution_count=user.execution_count,
            )

        strategy_examinator = AiQuotaStrategyExaminator(executor=user)
        user.execution_count.remaining_quotas["ai"] = strategy_examinator.get_quotas()
        self.update(user)
        user = self._user_repository.get_by_id(id=user_id)
        assert user is not None
        return Userinfo(
            name=user.google_userinfo.name,
            avatar_url=user.google_userinfo.picture,
            execution_count=user.execution_count,
        )
