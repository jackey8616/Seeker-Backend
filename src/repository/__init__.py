from abc import ABC
from typing import Generic, Optional, TypeVar, cast, get_args

from bson import ObjectId
from kink import di
from pydantic import BaseModel, TypeAdapter
from pymongo import MongoClient
from pymongo.collection import Collection

T = TypeVar("T", bound=BaseModel)


class Repository(ABC, Generic[T]):
    @property
    def _table_name(self) -> str:
        raise NotImplementedError()

    @property
    def _client(self):
        return MongoClient(di["MONGODB_ENDPOINT"])

    @property
    def _table(self) -> Collection:
        return self._client.get_database(name=di["MONGODB_DATABASE"]).get_collection(
            name=self._table_name
        )

    def get_by_id(self, id: str) -> Optional[T]:
        raw_document = self._table.find_one({"_id": ObjectId(id)})
        if raw_document is None:
            return None

        origin_bases = cast(list, getattr(self, "__orig_bases__")) or []  # noqa: B009
        generic_types = get_args(origin_bases[0])
        generic_type = generic_types[0]
        return TypeAdapter(type=generic_type).validate_python(raw_document)

    def insert_one(self, obj: T) -> T:
        result = self._table.insert_one(obj.model_dump(by_alias=True, exclude={"id"}))
        inserted_obj = self.get_by_id(id=result.inserted_id)
        if inserted_obj is None:
            raise ValueError("Insert failed")
        return inserted_obj
