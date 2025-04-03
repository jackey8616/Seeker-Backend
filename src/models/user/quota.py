from pydantic import BaseModel


class ModelQuota(BaseModel):
    name: str
    maximum_amount: int
    remaining_amount: int
