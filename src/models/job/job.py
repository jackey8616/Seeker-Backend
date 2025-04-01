from datetime import datetime, timezone

from pydantic import Field

from models import MongoDocument
from models.job.company import ModelCompany
from utils.typings import PyObjectId


class ModelJob(MongoDocument):
    domain: str
    url: str
    title: str
    location: str
    company: ModelCompany
    salary: str
    work_type: str
    description: str
    description_hash: str
    updated_at: datetime
    created_at: datetime = Field(default=datetime.now(tz=timezone.utc))
    chat_log_ids: list[PyObjectId] = Field(default=[])
