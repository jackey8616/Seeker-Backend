from typing import Optional

from pydantic import BaseModel, Field


class ListMailsRequestDto(BaseModel):
    next_page_token: Optional[str] = Field(default=None)
