from dataclasses import dataclass

from dtos.repository.cursor import Cursor
from dtos.responses.api_response import ApiResponseDto
from services.job.models import Job


@dataclass
class GetJobsResponseDto(ApiResponseDto):
    jobs: list[Job]
    cursor: Cursor

    @property
    def data(self):
        return {
            "jobs": self.jobs,
            "cursor": self.cursor,
        }
