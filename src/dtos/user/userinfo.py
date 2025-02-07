from pydantic import BaseModel


class Userinfo(BaseModel):
    name: str
