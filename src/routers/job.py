from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from dtos.auth.auth_dtos import TokenData
from request.job.crawl_job import CrawlJobRequestDto
from request.job.get_jobs import GetJobsRequestDto
from request.job.job_fitting_ai_by_url import JobFittingAiByUrlRequestDto
from responses.job.crawl_job import CrawlJobResponseDto
from responses.job.fitting_ai_by_url import JobFittingAiByUrlResponseDto
from responses.job.get_job import GetJobResponseDto
from responses.job.get_jobs import GetJobsResponseDto
from services.auth.auth_bearer import JwtBearer
from services.job import JobService
from services.pipeline.flow.seek_au.match_resume_and_job_description import (
    MatchResumeAndJobDescriptionDataType,
    MatchResumeAndJobDescriptionStep,
)

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


@jobs_router.post(
    path="/fitting_by_ai/url",
    response_model=JobFittingAiByUrlResponseDto,
)
async def fitting_ai_by_url(
    request: JobFittingAiByUrlRequestDto,
    token_data: TokenData = Depends(JwtBearer(TokenData)),
    job_service: JobService = Depends(lambda: JobService()),
):
    user_id = token_data.sub
    model_job = job_service.upsert_job_from_url(link=request.url)
    if isinstance(model_job, (ValueError, RuntimeError)):
        raise ValueError(str(model_job))

    assert model_job.id is not None
    step = MatchResumeAndJobDescriptionStep()
    result = step.perform(
        data=MatchResumeAndJobDescriptionDataType(
            executor_id=user_id,
            restriction=request.restriction,
            resume=request.resume,
            job_ids=[model_job.id],
        ),
        next=lambda x: x,
        final=lambda x: x,
    )

    if isinstance(result, Exception):
        raise result

    data = result["fitting_result"][0]
    return JobFittingAiByUrlResponseDto(
        job_id=data["job_id"],
        chat_log_id=data["chat_log_id"],
        link=data["link"],
        ai_response=data["ai_response"],
    ).response()


@jobs_router.post("/fitting_by_ai/{job_id}")
async def fitting_ai_by_id(
    job_id: str,
    request: Request,
    token_data: TokenData = Depends(JwtBearer(TokenData)),
):
    user_id = token_data.sub
    json_data = await request.json()
    restriction = json_data["restriction"]
    resume = json_data["resume"]

    step = MatchResumeAndJobDescriptionStep()
    result = step.perform(
        data=MatchResumeAndJobDescriptionDataType(
            executor_id=user_id,
            restriction=restriction,
            resume=resume,
            job_ids=[job_id],
        ),
        next=lambda x: x,
        final=lambda x: x,
    )

    if isinstance(result, Exception):
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder({"error": repr(result)}),
        )

    assert isinstance(result, dict)
    return JSONResponse(
        content=jsonable_encoder(
            {
                "result": result["fitting_result"],
            }
        )
    )


@jobs_router.get(
    path="/{job_id}",
    response_model=GetJobResponseDto,
)
async def get_job(
    job_id: str,
    token_data: TokenData = Depends(JwtBearer(TokenData)),
    job_service: JobService = Depends(lambda: JobService()),
):
    model_job = job_service.get_by_id(executor_id=token_data.sub, job_id=job_id)
    if model_job is None:
        raise ValueError("Job not found")
    return GetJobResponseDto(job=model_job).response()
