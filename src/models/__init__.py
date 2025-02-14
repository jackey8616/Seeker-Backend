from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from utils.typings import PyObjectId


class MongoDocument(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
