from datetime import datetime

from pydantic import BaseModel


class AiChatLog(BaseModel):
    input: str
    output: str
    input_token: int
    output_token: int
    start_datetime: datetime
    end_datetime: datetime
