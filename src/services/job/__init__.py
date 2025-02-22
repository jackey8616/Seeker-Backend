from dataclasses import dataclass, field
from datetime import datetime, timezone
from hashlib import md5

from services.job.crawler.dtos import CrawledJob
from services.job.dtos import Company
from services.job.models import Job
from services.job.repository import JobRepository


@dataclass
class JobService:
    _job_repository: JobRepository = field(default_factory=lambda: JobRepository())

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

    def get_many(self) -> list[Job]:
        return self._job_repository.get_many()
