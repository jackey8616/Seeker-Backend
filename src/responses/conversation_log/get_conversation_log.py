from dataclasses import dataclass
from typing import Optional

from dtos.ai.ai_conversation_log import AiConversationLog
from responses.api_response import ApiResponseDto


@dataclass
class GetConversationLogResponseDto(ApiResponseDto):
    log: Optional[AiConversationLog]

    @property
    def data(self):
        return {"log": self.log}
