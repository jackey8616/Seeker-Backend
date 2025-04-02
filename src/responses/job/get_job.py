from dataclasses import dataclass

from responses.api_response import ApiResponseDto
from services.job.dtos.job_dto import JobDto


@dataclass
class GetJobResponseDto(ApiResponseDto):
    job: JobDto

    @property
    def data(self):
        return {
            "job": self.job,
        }
