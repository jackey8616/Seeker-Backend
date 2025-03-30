from pydantic import BaseModel


class MailInfo(BaseModel):
    id: str
    snippet: str
