from dataclasses import dataclass

from dtos.repository.cursor import Cursor
from dtos.responses.api_response import ApiResponseDto
from dtos.responses.job import JobDto


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
