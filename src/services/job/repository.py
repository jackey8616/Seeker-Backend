from dataclasses import dataclass
from typing import Optional

from bson import ObjectId

from dtos.repository.order_by import OrderBy
from dtos.repository.paginator import Paginator
from repository import Repository
from services.job.models import Job


@dataclass
class JobRepository(Repository[Job]):
    @property
    def _table_name(self) -> str:
        return "jobs"

    def get_by_url(self, url: str) -> Optional[Job]:
        raw_document = self._table.find_one({"url": url})
        if raw_document is None:
            return None
        return Job.model_validate(obj=raw_document)

    def get_many(self, paginator_token: Optional[str]) -> tuple[list[Job], Paginator]:
        paginator = (
            Paginator(order_by=OrderBy.DESC, n=self._default_page_size)
            if paginator_token is None
            else Paginator.decode(
                paginator_token=paginator_token,
                max_n=self._max_page_size,
                default_n=self._default_page_size,
            )
        )

        raw_documents = (
            self._table.find(paginator.condition)
            .sort(paginator.sort)
            .limit(paginator.n)
        )

        return (
            [Job.model_validate(obj=raw_document) for raw_document in raw_documents],
            paginator,
        )

    def upsert(self, job: Job) -> Job | ValueError:
        result = self._table.update_one(
            filter={"url": job.url},
            update={
                "$set": job.model_dump(
                    by_alias=True,
                    exclude={"id", "created_at"},
                ),
                "$setOnInsert": {
                    "created_at": job.created_at,
                },
            },
            upsert=True,
        )

        upserted_obj = (
            self.get_by_id(id=result.upserted_id)
            if result.did_upsert is True
            else self.get_by_url(url=job.url)
        )

        if upserted_obj is None:
            return ValueError("Upsert failed")
        return upserted_obj

    def update(self, job: Job):
        self._table.find_one_and_update(
            filter={"_id": ObjectId(job.id)},
            update={
                "$set": job.model_dump(
                    by_alias=True,
                    exclude={"id"},
                ),
            },
        )
