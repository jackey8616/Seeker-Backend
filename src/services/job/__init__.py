from dataclasses import dataclass, field
from hashlib import md5

from services.job.crawler.dtos import CrawledJob
from services.job.dtos import Company
from services.job.models import Job
from services.job.repository import JobRepository


@dataclass
class JobService:
    _job_repository: JobRepository = field(default_factory=lambda: JobRepository())

    def is_job_url_exists(self, url: str) -> bool:
        return self._job_repository.get_by_url(url=url) is not None

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
        )
        return self._job_repository.upsert(job=model_job)
