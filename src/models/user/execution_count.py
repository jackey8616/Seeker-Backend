from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from models.user.quota import ModelQuota


class ModelExecutionCount(BaseModel):
    total_count: int = Field(default=0)
    nearest_execution_datetimes: list[datetime] = Field(default_factory=list)
    last_execution_datetime: Optional[datetime] = Field(default=None)
    remaining_quotas: dict[str, list[ModelQuota]] = Field(default_factory=dict)
