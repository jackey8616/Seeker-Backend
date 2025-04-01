from dataclasses import dataclass
from typing import Optional

from responses.api_response import ApiResponseDto
from services.ai.dtos.ai_conversation_log import AiConversationLog


@dataclass
class GetConversationLogResponseDto(ApiResponseDto):
    log: Optional[AiConversationLog]

    @property
    def data(self):
        return {"log": self.log}
