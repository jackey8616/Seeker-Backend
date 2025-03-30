from dataclasses import dataclass

from repository.cursor import Cursor
from responses.api_response import ApiResponseDto
from services.job.dtos.job_dto import JobDto


@dataclass
class GetJobsResponseDto(ApiResponseDto):
    jobs: list[JobDto]
    cursor: Cursor

    @property
    def data(self):
        return {
            "jobs": self.jobs,
            "cursor": self.cursor,
        }
