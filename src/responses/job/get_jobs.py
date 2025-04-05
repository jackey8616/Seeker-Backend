from dataclasses import dataclass

from dtos.job.job_dtos import JobDto
from repository.cursor import Cursor
from responses.api_response import ApiResponseDto


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
