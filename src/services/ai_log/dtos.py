from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.ai_chat_log import ModelAiChatLog


class AiConversationLog(BaseModel):
    executor_id: str
    model_name: str
    system_instruction: list[str]
    chats: list[ModelAiChatLog]
    total_input_token: int
    total_output_token: int
    created_at: datetime
    id: str = Field(alias="_id")
    updated_at: Optional[datetime] = Field(default=None)
    model_config = ConfigDict(populate_by_name=True)
