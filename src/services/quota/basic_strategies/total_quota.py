from dataclasses import dataclass

from models.user.execution_count import ModelExecutionCount
from models.user.quota import ModelQuota
from services.quota import QuotaStrategy


@dataclass
class TotalQuotaStrategy(QuotaStrategy):
    """Strategy that limits AI service usage to a certain total number of calls."""

    def __init__(self, total_limit: int):
        super().__init__(name="total", amount=total_limit)

    def is_exceed(self, execution_count: ModelExecutionCount) -> bool:
        return execution_count.total_count >= self.amount

    def get_quota(self, execution_count: ModelExecutionCount) -> ModelQuota:
        used_quota = execution_count.total_count
        return ModelQuota(
            name=self.name,
            maximum_amount=self.amount,
            remaining_amount=max(0, self.amount - used_quota),
        )
