from kink import di
from pytest import fixture


class UnitTestCase:
    @fixture(autouse=True)
    def setup_fixture(self):
        di["MAXIMUM_AI_CHAT_RECORD_LIMIT"] = 200
        di["AI_QUOTA_HOURLY_LIMIT"] = 10000
        di["AI_QUOTA_DAILY_LIMIT"] = 100000
        di["AI_QUOTA_MONTHLY_LIMIT"] = 10000
