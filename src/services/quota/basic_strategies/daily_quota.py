from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from models.user.execution_count import ModelExecutionCount
from models.user.quota import ModelQuota
from services.quota import QuotaStrategy


@dataclass
class DailyQuotaStrategy(QuotaStrategy):
    """Strategy that limits AI service usage to a certain number of calls per day."""

    def __init__(self, daily_limit: int):
        super().__init__(name="daily", amount=daily_limit)

    def is_exceed(self, execution_count: ModelExecutionCount) -> bool:
        nearest_execution_datetimes = sorted(
            execution_count.nearest_execution_datetimes
        )
        if nearest_execution_datetimes is None or len(nearest_execution_datetimes) == 0:
            return False

        previous_day_execution_datetimes = [
            dt
            for dt in nearest_execution_datetimes
            if dt >= (datetime.now(tz=timezone.utc) - timedelta(days=1))
        ]

        return len(previous_day_execution_datetimes) >= self.amount

    def get_quota(self, execution_count: ModelExecutionCount) -> ModelQuota:
        nearest_execution_datetimes = sorted(
            execution_count.nearest_execution_datetimes
        )
        if nearest_execution_datetimes is None or len(nearest_execution_datetimes) == 0:
            return ModelQuota(
                name=self.name, maximum_amount=self.amount, remaining_amount=self.amount
            )

        previous_day_execution_datetimes = [
            dt
            for dt in nearest_execution_datetimes
            if dt >= (datetime.now(tz=timezone.utc) - timedelta(days=1))
        ]

        used_quota = len(previous_day_execution_datetimes)
        return ModelQuota(
            name=self.name,
            maximum_amount=self.amount,
            remaining_amount=max(0, self.amount - used_quota),
        )
