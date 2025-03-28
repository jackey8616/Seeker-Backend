from datetime import datetime
from typing import Optional

from pydantic import Field

from models import MongoDocument
from utils.typings import PyObjectId


class AiConversationLog(MongoDocument):
    executor_id: str
    model_name: str
    system_instruction: list[str]
    chats: list[PyObjectId]
    total_input_token: int
    total_output_token: int
    created_at: datetime
    updated_at: Optional[datetime] = Field(default=None)
