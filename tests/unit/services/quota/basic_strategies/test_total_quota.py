from pytest import fixture

from models.user.execution_count import ModelExecutionCount
from models.user.quota import ModelQuota
from services.quota.basic_strategies.total_quota import TotalQuotaStrategy
from tests.unit import UnitTestCase


class TestTotalQuotaStrategy(UnitTestCase):
    @fixture
    def strategy(self) -> TotalQuotaStrategy:
        return TotalQuotaStrategy(total_limit=10)

    @fixture
    def execution_count(self) -> ModelExecutionCount:
        return ModelExecutionCount(total_count=5, nearest_execution_datetimes=[])

    def test_is_exceed_when_below_limit(
        self, strategy: TotalQuotaStrategy, execution_count: ModelExecutionCount
    ):
        assert not strategy.is_exceed(execution_count)

    def test_is_exceed_when_at_limit(
        self, strategy: TotalQuotaStrategy, execution_count: ModelExecutionCount
    ):
        execution_count = ModelExecutionCount(
            total_count=10, nearest_execution_datetimes=[]
        )
        assert strategy.is_exceed(execution_count)

    def test_is_exceed_when_above_limit(
        self, strategy: TotalQuotaStrategy, execution_count: ModelExecutionCount
    ):
        execution_count = ModelExecutionCount(
            total_count=11, nearest_execution_datetimes=[]
        )
        assert strategy.is_exceed(execution_count)

    def test_get_quota(
        self, strategy: TotalQuotaStrategy, execution_count: ModelExecutionCount
    ):
        quota = strategy.get_quota(execution_count)
        assert isinstance(quota, ModelQuota)
        assert quota.name == "total"
        assert quota.maximum_amount == 10
        assert quota.remaining_amount == 5
