from datetime import datetime, timezone

from pydantic import BaseModel, Field

from dtos.shared.company import Company
from models.ai_chat_log import ModelAiChatLog


class JobDto(BaseModel):
    domain: str
    url: str
    title: str
    location: str
    company: Company
    salary: str
    work_type: str
    description: str
    description_hash: str
    updated_at: datetime
    created_at: datetime = Field(default=datetime.now(tz=timezone.utc))
    chat_logs: list[ModelAiChatLog] = Field(default=[])
