from dataclasses import dataclass
from typing import Optional

from models.job.job import ModelJob
from repository import Repository


@dataclass
class JobRepository(Repository[ModelJob]):
    @property
    def _table_name(self) -> str:
        return "jobs"

    def get_by_url(self, url: str) -> Optional[ModelJob]:
        raw_document = self._table.find_one({"url": url})
        if raw_document is None:
            return None
        return ModelJob.model_validate(obj=raw_document)

    def upsert(self, job: ModelJob) -> ModelJob | ValueError:
        result = self._table.update_one(
            filter={"url": job.url},
            update={
                "$set": job.model_dump(
                    by_alias=True,
                    exclude={"id", "created_at", "chat_log_ids"},
                ),
                "$setOnInsert": {
                    "created_at": job.created_at,
                    "chat_log_ids": job.chat_log_ids,
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
