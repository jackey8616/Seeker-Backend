from typing import Optional

from pydantic import BaseModel


class ModelCompany(BaseModel):
    name: str
    link: Optional[str]
