from dataclasses import dataclass

from models.job.job import ModelJob
from responses.api_response import ApiResponseDto


@dataclass
class CrawlJobResponseDto(ApiResponseDto):
    job: ModelJob

    @property
    def data(self):
        return {
            "job": self.job,
        }
