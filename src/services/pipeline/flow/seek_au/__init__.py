from dataclasses import dataclass

from services.pipeline import Pipeline
from services.pipeline.flow.seek_au.crawl_from_links_step import CrawlFromLinksStep
from services.pipeline.flow.seek_au.extract_link_from_mail_step import (
    ExtractLinkFromMailStep,
)
from services.pipeline.flow.seek_au.match_resume_and_job_description import (
    MatchResumeAndJobDescriptionStep,
)


@dataclass(kw_only=True)
class SeekAuPipeline(Pipeline):
    def __post_init__(self):
        self.through(
            [
                ExtractLinkFromMailStep(),
                CrawlFromLinksStep(),
                MatchResumeAndJobDescriptionStep(),
            ]
        )
