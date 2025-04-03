from typing import Optional

from pydantic import BaseModel

from models.user.execution_count import ModelExecutionCount


class Userinfo(BaseModel):
    name: str
    avatar_url: Optional[str]
    execution_count: Optional[ModelExecutionCount]
