from dataclasses import dataclass

from repository.cursor import Cursor
from responses.api_response import ApiResponseDto
from services.ai_log.dtos import AiConversationLog


@dataclass
class GetConversationLogsResponseDto(ApiResponseDto):
    logs: list[AiConversationLog]
    cursor: Cursor

    @property
    def data(self):
        return {
            "logs": self.logs,
            "cursor": self.cursor,
        }
