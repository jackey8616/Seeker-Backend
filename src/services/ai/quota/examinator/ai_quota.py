from dataclasses import dataclass, field

from kink import di

from models.user.user import ModelUser
from services.ai.quota import QuotaStrategy
from services.ai.quota.basic_strategies.daily_quota import DailyQuotaStrategy
from services.ai.quota.basic_strategies.hourly_quota import HourlyQuotaStrategy
from services.ai.quota.basic_strategies.monthly_quota import MonthlyQuotaStrategy
from services.ai.quota.examinator import QuotaExaminator


@dataclass
class AiQuotaStrategyExaminator(QuotaExaminator):
    executor: ModelUser
    name: str = "ai"
    strategies: list[QuotaStrategy] = field(
        default_factory=lambda: [
            HourlyQuotaStrategy(hourly_limit=di["AI_QUOTA_HOURLY_LIMIT"]),
            DailyQuotaStrategy(daily_limit=di["AI_QUOTA_DAILY_LIMIT"]),
            MonthlyQuotaStrategy(monthly_limit=di["AI_QUOTA_MONTHLY_LIMIT"]),
        ],
    )
