from fastapi import APIRouter, Depends

from dtos.auth.token import TokenData
from dtos.request.job.get_jobs import GetJobsRequestDto
from dtos.responses.job.get_jobs import GetJobsResponseDto
from services.auth.auth_bearer import JwtBearer
from services.job import JobService

jobs_router = APIRouter(
    prefix="/jobs",
    tags=["Job"],
)


@jobs_router.post(
    path="/",
    response_model=GetJobsResponseDto,
)
async def get_jobs(
    request: GetJobsRequestDto,
    _: TokenData = Depends(JwtBearer(TokenData)),
    job_service: JobService = Depends(lambda: JobService()),
):
    paginator_token = request.page_token
    (job_dtos, cursor) = job_service.get_many(paginator_token=paginator_token)
    return GetJobsResponseDto(jobs=job_dtos, cursor=cursor).response()
