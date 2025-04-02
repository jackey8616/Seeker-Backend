from datetime import datetime, timezone

from pydantic import BaseModel, Field

from models.ai.ai_chat_log import ModelAiChatLog
from models.job.company import ModelCompany


class JobDto(BaseModel):
    id: str
    domain: str
    url: str
    title: str
    location: str
    company: ModelCompany
    salary: str
    work_type: str
    description: str
    raw_description: str
    description_hash: str
    updated_at: datetime
    created_at: datetime = Field(default=datetime.now(tz=timezone.utc))
    chat_logs: list[ModelAiChatLog] = Field(default=[])
