from abc import ABC
from dataclasses import dataclass
from typing import ClassVar, Generic, Optional, TypeVar, cast, get_args

from bson import ObjectId
from kink import di
from pydantic import TypeAdapter
from pymongo import MongoClient
from pymongo.collection import Collection

from models import MongoDocument
from repository.order_by import OrderBy
from repository.paginator import Paginator

T = TypeVar("T", bound=MongoDocument)


@dataclass
class Repository(ABC, Generic[T]):
    _default_page_size: ClassVar[int] = 20
    _max_page_size: ClassVar[int] = 100

    @property
    def _table_name(self) -> str:
        raise NotImplementedError()

    @property
    def _client(self):
        return MongoClient(di["MONGODB_ENDPOINT"], tz_aware=True)

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

    def get_many(
        self,
        query: dict,
        paginator_token: Optional[str] = None,
        order_by: OrderBy = OrderBy.DESC,
    ) -> tuple[list[T], Paginator]:
        """Get many documents with pagination support.

        Args:
            query: MongoDB query
            paginator_token: Optional pagination token
            order_by: Sort order, defaults to DESC

        Returns:
            Tuple of (documents, paginator)
        """
        paginator = (
            Paginator(order_by=order_by, n=self._default_page_size)
            if paginator_token is None
            else Paginator.decode(
                paginator_token=paginator_token,
                max_n=self._max_page_size,
                default_n=self._default_page_size,
            )
        )

        query.update(paginator.condition)

        raw_documents = list(
            self._table.find(query).sort(paginator.sort).limit(paginator.n + 1)
        )
        if len(raw_documents) > paginator.n:
            raw_documents = raw_documents[:-1]

        origin_bases = cast(list, getattr(self, "__orig_bases__")) or []  # noqa: B009
        generic_types = get_args(origin_bases[0])
        generic_type = generic_types[0]

        return (
            [
                TypeAdapter(type=generic_type).validate_python(raw_document)
                for raw_document in raw_documents
            ],
            paginator,
        )

    def update(self, obj: T):
        self._table.find_one_and_update(
            filter={"_id": ObjectId(obj.id)},
            update={
                "$set": obj.model_dump(
                    by_alias=True,
                    exclude={"id"},
                ),
            },
        )
