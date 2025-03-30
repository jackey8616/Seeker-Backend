from base64 import b64decode, b64encode
from typing import Any, Mapping, Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from repository.order_by import OrderBy


class Paginator(BaseModel):
    order_by: OrderBy
    n: int
    start_id: Optional[str] = Field(default=None)

    def encode(self) -> str:
        return b64encode(self.model_dump_json().encode()).decode()

    @staticmethod
    def decode(
        paginator_token: str, max_n: int = 20, default_n: int = 20
    ) -> "Paginator":
        paginator = Paginator.model_validate_json(b64decode(paginator_token))
        if paginator.n > max_n:
            paginator.n = default_n
        return paginator

    @property
    def condition(self) -> Mapping[str, Any]:
        if self.start_id is None:
            return {}

        return {
            "_id": (
                {"$lt": ObjectId(self.start_id)}
                if self.order_by == OrderBy.DESC
                else {"$gt": ObjectId(self.start_id)}
            )
        }

    @property
    def sort(self) -> Mapping[str, Any]:
        return {"_id": -1 if self.order_by == OrderBy.DESC else 1}
