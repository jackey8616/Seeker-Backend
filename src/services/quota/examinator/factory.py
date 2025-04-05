from typing import Optional

from models.user.user import ModelUser
from services.quota.examinator import QuotaExaminator
from services.quota.examinator.ai_quota import AiQuotaStrategyExaminator


class StrategyExaminatorFactory:
    @staticmethod
    def get_examinator(name: str, executor: ModelUser) -> Optional[QuotaExaminator]:
        match name:
            case "ai":
                return AiQuotaStrategyExaminator(executor=executor)
            case _:
                return None
