from datetime import datetime, timedelta, timezone

from pytest import fixture

from models.user.execution_count import ModelExecutionCount
from services.quota.basic_strategies.daily_quota import DailyQuotaStrategy
from tests.unit import UnitTestCase


class TestDailyQuotaStrategy(UnitTestCase):
    @fixture
    def strategy(self) -> DailyQuotaStrategy:
        return DailyQuotaStrategy(daily_limit=100)

    @fixture
    def current_time(self) -> datetime:
        return datetime.now(tz=timezone.utc)

    def test_is_exceed_when_empty_executions(self, strategy: DailyQuotaStrategy):
        execution_count = ModelExecutionCount(
            total_count=0, nearest_execution_datetimes=[]
        )
        assert not strategy.is_exceed(execution_count)

    def test_is_exceed_when_below_limit(
        self, strategy: DailyQuotaStrategy, current_time: datetime
    ):
        datetimes = [current_time - timedelta(hours=i) for i in range(10)]
        execution_count = ModelExecutionCount(
            total_count=10, nearest_execution_datetimes=datetimes
        )
        assert not strategy.is_exceed(execution_count)

    def test_is_exceed_when_at_limit(
        self, strategy: DailyQuotaStrategy, current_time: datetime
    ):
        datetimes = [current_time - timedelta(minutes=i) for i in range(100)]
        execution_count = ModelExecutionCount(
            total_count=100, nearest_execution_datetimes=datetimes
        )
        assert strategy.is_exceed(execution_count)

    def test_is_exceed_when_old_executions(
        self, strategy: DailyQuotaStrategy, current_time: datetime
    ):
        datetimes = [current_time - timedelta(days=2) for _ in range(200)]
        execution_count = ModelExecutionCount(
            total_count=200, nearest_execution_datetimes=datetimes
        )
        assert not strategy.is_exceed(execution_count)

    def test_get_quota_when_empty(self, strategy: DailyQuotaStrategy):
        execution_count = ModelExecutionCount(
            total_count=0, nearest_execution_datetimes=[]
        )
        quota = strategy.get_quota(execution_count)
        assert quota.remaining_amount == 100
        assert quota.maximum_amount == 100

    def test_get_quota_with_recent_executions(
        self, strategy: DailyQuotaStrategy, current_time: datetime
    ):
        datetimes = [current_time - timedelta(hours=i) for i in range(50)]
        execution_count = ModelExecutionCount(
            total_count=50, nearest_execution_datetimes=datetimes
        )
        quota = strategy.get_quota(execution_count)
        assert quota.remaining_amount == 76
        assert quota.maximum_amount == 100
