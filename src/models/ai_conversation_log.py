from datetime import datetime
from typing import Optional

from pydantic import Field

from dtos.google.vertex import AiChatLog
from models import MongoDocument


class AiConversationLog(MongoDocument):
    model_name: str
    system_instruction: list[str]
    chats: list[AiChatLog]
    total_input_token: int
    total_output_token: int
    created_at: datetime
    updated_at: Optional[datetime] = Field(default=None)
