from datetime import datetime
from typing import Optional

from pydantic import Field

from models import MongoDocument
from utils.typings import PyObjectId


class ModelAiConversationLog(MongoDocument):
    executor_id: PyObjectId
    model_name: str
    system_instruction: list[str]
    chat_ids: list[PyObjectId]
    total_input_token: int
    total_output_token: int
    created_at: datetime
    updated_at: Optional[datetime] = Field(default=None)
