from datetime import datetime, timezone

from pydantic import Field

from dtos.shared.company import Company
from models import MongoDocument
from utils.typings import PyObjectId


class ModelJob(MongoDocument):
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
    chat_log_ids: list[PyObjectId] = Field(default=[])
