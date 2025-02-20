from datetime import datetime
from typing import Any

from pydantic import Field

from models import MongoDocument
from utils.typings import PyObjectId


class AiChatLog(MongoDocument):
    conversation_id: PyObjectId
    input: str
    output: str
    input_token: int
    output_token: int
    start_datetime: datetime
    end_datetime: datetime
    metrics: dict[str, Any] = Field(default={})
