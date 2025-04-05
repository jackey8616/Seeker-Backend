from typing import Optional

from pydantic import BaseModel

from models.user.execution_count import ModelExecutionCount


class TokenData(BaseModel):
    sub: str


class Userinfo(BaseModel):
    name: str
    avatar_url: Optional[str]
    execution_count: Optional[ModelExecutionCount]
