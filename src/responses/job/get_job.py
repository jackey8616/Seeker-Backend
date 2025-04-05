from dataclasses import dataclass

from dtos.job.job_dtos import JobDto
from responses.api_response import ApiResponseDto


@dataclass
class GetJobResponseDto(ApiResponseDto):
    job: JobDto

    @property
    def data(self):
        return {
            "job": self.job,
        }
