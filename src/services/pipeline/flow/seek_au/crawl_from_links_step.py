from dataclasses import dataclass

from services.job import JobService
from services.job.crawler.factory import CrawlerFactory
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
            crawler = CrawlerFactory.get_crawler(link=link)
            if crawler is None:
                warning(f"Crawler for {link} is not found.")
                continue

            crawled_job = crawler.crawl()
            if isinstance(crawled_job, (ValueError, RuntimeError)):
                warning(f"Crawling failed: {repr(crawled_job)}")
                continue

            model_job = service.upsert_crawled_job(job=crawled_job)
            if isinstance(model_job, ValueError):
                warning("Upsert job failed.")
                continue
            assert model_job.id is not None
            job_ids.append(model_job.id)

        pass_data = data.model_dump() | {
            "job_ids": job_ids,
        }
        return next(pass_data)
