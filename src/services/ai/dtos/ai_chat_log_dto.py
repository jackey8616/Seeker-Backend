from datetime import datetime
from typing import Any

from pydantic import BaseModel


class AiChatLogDto(BaseModel):
    id: str
    executor_id: str
    conversation_id: str
    input: str
    output: str
    input_token: int
    output_token: int
    start_datetime: datetime
    end_datetime: datetime
    metrics: dict[str, Any] = {}
