from fastapi import APIRouter, Depends

from dtos.auth.token import TokenData
from dtos.responses.job.get_jobs import GetJobsResponseDto
from services.auth.auth_bearer import JwtBearer
from services.job import JobService

jobs_router = APIRouter(
    prefix="/jobs",
    tags=["Job"],
)


@jobs_router.get(
    path="/",
)
async def get_jobs(
    _: TokenData = Depends(JwtBearer(TokenData)),
    job_service: JobService = Depends(lambda: JobService()),
):
    jobs = job_service.get_many()
    return GetJobsResponseDto(jobs=jobs).response()
