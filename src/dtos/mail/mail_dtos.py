from datetime import datetime

from pydantic import BaseModel


class MailInfo(BaseModel):
    id: str
    snippet: str


class Mail(MailInfo):
    title: str
    sender: str
    date: datetime
    is_extracted: bool
    extracted_data: str
