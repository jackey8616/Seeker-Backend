from dataclasses import dataclass

from dtos.ai_log.ai_conversation_log import AiConversationLog
from dtos.responses.api_response import ApiResponseDto


@dataclass
class GetConversationLogsResponseDto(ApiResponseDto):
    logs: list[AiConversationLog]

    @property
    def data(self):
        return {"logs": self.logs}
