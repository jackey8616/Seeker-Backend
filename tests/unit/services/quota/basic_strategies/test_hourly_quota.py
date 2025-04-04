from datetime import datetime, timedelta, timezone

from pytest import fixture

from models.user.execution_count import ModelExecutionCount
from services.quota.basic_strategies.hourly_quota import HourlyQuotaStrategy
from tests.unit import UnitTestCase


class TestHourlyQuotaStrategy(UnitTestCase):
    @fixture
    def strategy(self) -> HourlyQuotaStrategy:
        return HourlyQuotaStrategy(hourly_limit=5)

    @fixture
    def current_time(self) -> datetime:
        return datetime.now(tz=timezone.utc)

    def test_is_exceed_when_empty_executions(self, strategy: HourlyQuotaStrategy):
        execution_count = ModelExecutionCount(
            total_count=0, nearest_execution_datetimes=[]
        )
        assert not strategy.is_exceed(execution_count)

    def test_is_exceed_when_below_limit(
        self, strategy: HourlyQuotaStrategy, current_time: datetime
    ):
        datetimes = [current_time - timedelta(minutes=i) for i in range(3)]
        execution_count = ModelExecutionCount(
            total_count=3, nearest_execution_datetimes=datetimes
        )
        assert not strategy.is_exceed(execution_count)

    def test_is_exceed_when_at_limit(
        self, strategy: HourlyQuotaStrategy, current_time: datetime
    ):
        datetimes = [current_time - timedelta(minutes=i) for i in range(5)]
        execution_count = ModelExecutionCount(
            total_count=5, nearest_execution_datetimes=datetimes
        )
        assert strategy.is_exceed(execution_count)

    def test_is_exceed_when_above_limit(
        self, strategy: HourlyQuotaStrategy, current_time: datetime
    ):
        datetimes = [current_time - timedelta(minutes=i) for i in range(6)]
        execution_count = ModelExecutionCount(
            total_count=6, nearest_execution_datetimes=datetimes
        )
        assert strategy.is_exceed(execution_count)

    def test_is_exceed_when_old_executions(
        self, strategy: HourlyQuotaStrategy, current_time: datetime
    ):
        datetimes = [current_time - timedelta(hours=2) for _ in range(10)]
        execution_count = ModelExecutionCount(
            total_count=10, nearest_execution_datetimes=datetimes
        )
        assert not strategy.is_exceed(execution_count)

    def test_get_quota_when_empty(self, strategy: HourlyQuotaStrategy):
        execution_count = ModelExecutionCount(
            total_count=0, nearest_execution_datetimes=[]
        )
        quota = strategy.get_quota(execution_count)
        assert quota.remaining_amount == 5
        assert quota.maximum_amount == 5

    def test_get_quota_with_recent_executions(
        self, strategy: HourlyQuotaStrategy, current_time: datetime
    ):
        datetimes = [current_time - timedelta(minutes=i) for i in range(3)]
        execution_count = ModelExecutionCount(
            total_count=3, nearest_execution_datetimes=datetimes
        )
        quota = strategy.get_quota(execution_count)
        assert quota.remaining_amount == 2
        assert quota.maximum_amount == 5
