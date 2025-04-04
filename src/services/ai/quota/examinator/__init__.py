from abc import ABC
from dataclasses import dataclass

from models.user.execution_count import ModelExecutionCount
from models.user.quota import ModelQuota
from models.user.user import ModelUser
from services.ai.quota import QuotaStrategy
from services.ai.quota.exceptions import ExecutionQuotaExceedError


@dataclass
class QuotaExaminator(ABC):
    executor: ModelUser
    name: str
    strategies: list[QuotaStrategy]

    def is_exceed(self) -> bool:
        if self.executor.execution_count is None:
            return False
        return any(
            strategy.is_exceed(self.executor.execution_count)
            for strategy in self.strategies
        )

    def get_quotas(self) -> list[ModelQuota]:
        if self.executor.execution_count is None:
            return [
                strategy.get_quota(ModelExecutionCount())
                for strategy in self.strategies
            ]

        return [
            strategy.get_quota(self.executor.execution_count)
            for strategy in self.strategies
        ]

    def form_quota_error(self) -> ExecutionQuotaExceedError:
        return ExecutionQuotaExceedError(
            name=self.name, remaining_quotas=self.get_quotas()
        )
