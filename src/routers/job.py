from fastapi import APIRouter, Depends

from request.job.crawl_job import CrawlJobRequestDto
from request.job.get_jobs import GetJobsRequestDto
from responses.job.crawl_job import CrawlJobResponseDto
from responses.job.get_jobs import GetJobsResponseDto
from services.auth.auth_bearer import JwtBearer
from services.auth.dtos.token import TokenData
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
    token_data: TokenData = Depends(JwtBearer(TokenData)),
    job_service: JobService = Depends(lambda: JobService()),
):
    paginator_token = request.page_token
    (job_dtos, cursor) = job_service.get_many(
        executor_id=token_data.sub, paginator_token=paginator_token
    )
    return GetJobsResponseDto(jobs=job_dtos, cursor=cursor).response()


@jobs_router.post(
    path="/crawl",
    response_model=CrawlJobResponseDto,
)
async def crawl_job(
    request: CrawlJobRequestDto,
    token_data: TokenData = Depends(JwtBearer(TokenData)),
    job_service: JobService = Depends(lambda: JobService()),
):
    model_job = job_service.upsert_job_from_url(link=request.url)
    if isinstance(model_job, (ValueError, RuntimeError)):
        raise ValueError(str(model_job))
    return CrawlJobResponseDto(job=model_job).response()
