from dataclasses import dataclass, field
from datetime import datetime, timezone
from hashlib import md5
from typing import Optional

from models.job.company import ModelCompany
from models.job.job import ModelJob
from repository.ai_chat_log import AiChatLogRepository
from repository.cursor import Cursor
from repository.job import JobRepository
from services.job.crawler.factory import CrawlerFactory
from services.job.dtos.job_dto import JobDto
from services.job.transformer import JobDtoTransformer


@dataclass
class JobService:
    _job_repository: JobRepository = field(default_factory=lambda: JobRepository())
    _chat_log_repository: AiChatLogRepository = field(
        default_factory=lambda: AiChatLogRepository()
    )

    def upsert_job_from_url(self, link: str) -> ModelJob | ValueError | RuntimeError:
        crawler = CrawlerFactory.get_crawler(link=link)
        if crawler is None:
            return ValueError(f"Crawler for {link} is not found.")

        crawled_job = crawler.crawl()
        if isinstance(crawled_job, (ValueError, RuntimeError)):
            return crawled_job

        model_company = ModelCompany(
            name=crawled_job.company.name,
            link=crawled_job.company.link,
        )
        model_job = ModelJob(
            domain=crawled_job.domain,
            url=crawled_job.url,
            title=crawled_job.title,
            location=crawled_job.location,
            company=model_company,
            salary=crawled_job.salary,
            work_type=crawled_job.work_type,
            description=crawled_job.description,
            description_hash=md5(crawled_job.description.encode()).hexdigest(),
            updated_at=datetime.now(tz=timezone.utc),
        )
        model_job = self._job_repository.upsert(job=model_job)
        if isinstance(model_job, ValueError):
            return model_job
        assert model_job.id is not None
        return model_job

    def get_many(
        self, executor_id: str, paginator_token: Optional[str] = None
    ) -> tuple[list[JobDto], Cursor]:
        (jobs, paginator) = self._job_repository.get_many(
            query={}, paginator_token=paginator_token
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
