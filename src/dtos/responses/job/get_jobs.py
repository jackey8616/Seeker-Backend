from dataclasses import dataclass

from dtos.responses.api_response import ApiResponseDto
from services.job.models import Job


@dataclass
class GetJobsResponseDto(ApiResponseDto):
    jobs: list[Job]

    @property
    def data(self):
        return {"jobs": self.jobs}
