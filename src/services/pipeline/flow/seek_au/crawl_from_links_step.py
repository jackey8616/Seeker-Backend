from dataclasses import dataclass

from services.job import JobService
from services.pipeline.step import FinalStep, NextStep, Step, StepDataType
from utils.logger import warning


class CrawlFromLinksDataType(StepDataType):
    links: list[str]


@dataclass
class CrawlFromLinksStep(Step[CrawlFromLinksDataType]):
    def perform(self, data: CrawlFromLinksDataType, next: NextStep, final: FinalStep):
        links = data.links
        service = JobService()

        job_ids: list[str] = []
        for link in links:
            model_job = service.upsert_job_from_url(link=link)
            if isinstance(model_job, (ValueError, RuntimeError)):
                warning(f"Crawl job failed: {repr(model_job)}")
                continue
            assert model_job.id is not None
            job_ids.append(model_job.id)

        pass_data = data.model_dump() | {
            "job_ids": job_ids,
        }
        return next(pass_data)
