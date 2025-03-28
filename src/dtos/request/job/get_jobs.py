from typing import Optional

from pydantic import BaseModel, Field


class GetJobsRequestDto(BaseModel):
    page_token: Optional[str] = Field(default=None)
