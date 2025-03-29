from dataclasses import dataclass

from dtos.ai_log.ai_conversation_log import AiConversationLog
from dtos.repository.cursor import Cursor
from dtos.responses.api_response import ApiResponseDto


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
