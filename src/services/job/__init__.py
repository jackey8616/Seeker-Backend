from dataclasses import dataclass, field
from datetime import datetime, timezone
from hashlib import md5
from typing import Optional

from dtos.repository.cursor import Cursor
from dtos.responses.job import JobDto
from dtos.shared.company import Company
from repository.ai_chat_log import AiChatLogRepository
from services.job.crawler.dtos import CrawledJob
from services.job.models import Job
from services.job.repository import JobRepository
from services.job.transformer import JobDtoTransformer


@dataclass
class JobService:
    _job_repository: JobRepository = field(default_factory=lambda: JobRepository())
    _chat_log_repository: AiChatLogRepository = field(
        default_factory=lambda: AiChatLogRepository()
    )

    def upsert_crawled_job(self, job: CrawledJob) -> Job | ValueError:
        model_company = Company(
            name=job.company.name,
            link=job.company.link,
        )
        model_job = Job(
            domain=job.domain,
            url=job.url,
            title=job.title,
            location=job.location,
            company=model_company,
            salary=job.salary,
            work_type=job.work_type,
            description=job.description,
            description_hash=md5(job.description.encode()).hexdigest(),
            updated_at=datetime.now(tz=timezone.utc),
        )
        return self._job_repository.upsert(job=model_job)

    def get_many(
        self, executor_id: str, paginator_token: Optional[str] = None
    ) -> tuple[list[JobDto], Cursor]:
        (jobs, paginator) = self._job_repository.get_many(
            paginator_token=paginator_token
        )
        cursor = Cursor.from_paginator(paginator=paginator, sorted_results=jobs)

        job_dtos: list[JobDto] = []
        for job in jobs:
            chat_logs = self._chat_log_repository.get_many_by_ids(
                ids=job.chat_log_ids, executor_id=executor_id
            )
            job_dto = JobDtoTransformer(job=job, chat_logs=chat_logs).transform()
            job_dtos.append(job_dto)
        return (job_dtos, cursor)
