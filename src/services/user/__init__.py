from dataclasses import dataclass, field
from typing import Optional

from dtos.auth.auth_dtos import Userinfo
from models.user.user import ModelUser
from repository.user import UserRepository
from services.quota.examinator.factory import StrategyExaminatorFactory


@dataclass
class UserService:
    _user_repository: UserRepository = field(default_factory=lambda: UserRepository())

    def get_user_info(self, user_id: str) -> Optional[Userinfo]:
        user = self._user_repository.get_by_id(id=user_id)
        if user is None:
            return None

        user = self._update_user_execution_count(user=user)
        if user.execution_count is None:
            return Userinfo(
                name=user.google_userinfo.name,
                avatar_url=user.google_userinfo.picture,
                execution_count=user.execution_count,
            )

        self._user_repository.update(obj=user)
        return Userinfo(
            name=user.google_userinfo.name,
            avatar_url=user.google_userinfo.picture,
            execution_count=user.execution_count,
        )

    def _update_user_execution_count(self, user: ModelUser) -> ModelUser:
        if user.execution_count is None:
            return user

        remaining_quotas = {}
        for strategy_name, _ in user.execution_count.remaining_quotas.items():
            strategy_examinator = StrategyExaminatorFactory.get_examinator(
                name=strategy_name, executor=user
            )
            if strategy_examinator is None:
                continue

            remaining_quotas[strategy_name] = strategy_examinator.get_quotas()
        user.execution_count.remaining_quotas = remaining_quotas
        return user
