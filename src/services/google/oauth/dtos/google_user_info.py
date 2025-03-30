from pydantic import BaseModel


class GoogleUserInfo(BaseModel):
    id: str
    name: str
    family_name: str
    given_name: str
    picture: str
