from pydantic import BaseModel


class TokenData(BaseModel):
    sub: str
