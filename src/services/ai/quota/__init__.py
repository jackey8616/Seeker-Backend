from abc import ABC, abstractmethod
from dataclasses import dataclass

from kink import di

from models.user.execution_count import ModelExecutionCount
from models.user.quota import ModelQuota
from utils.logger import warning


@dataclass
class QuotaStrategy(ABC):
    name: str
    amount: int

    def __post_init__(self):
        maximum_ai_chat_record_limit = di["MAXIMUM_AI_CHAT_RECORD_LIMIT"]
        if self.amount > maximum_ai_chat_record_limit:
            warning(
                f"Strategy {self.name}'s amount greater {self.amount} than MAXIMUM_AI_CHAT_RECORD_LIMIT {maximum_ai_chat_record_limit} would not properly functional."
            )

    @abstractmethod
    def is_exceed(self, execution_count: ModelExecutionCount) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get_quota(self, execution_count: ModelExecutionCount) -> ModelQuota:
        raise NotImplementedError()
