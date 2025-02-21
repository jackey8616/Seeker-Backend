from typing import Optional

from pydantic import BaseModel


class Company(BaseModel):
    name: str
    link: Optional[str]
