from dataclasses import dataclass

from dtos.responses.api_response import ApiResponseDto
from models.ai_conversation_log import AiConversationLog


@dataclass
class GetConversationLogsResponseDto(ApiResponseDto):
    logs: list[AiConversationLog]

    @property
    def data(self):
        return {"logs": self.logs}
