from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from request.mail.list_mails import ListMailsRequestDto
from responses.mail.get_mail import GetMailResponseDto
from responses.mail.list_mails import ListMailInfosResponseDto
from services.auth.auth_bearer import JwtBearer
from services.auth.dtos.token import TokenData
from services.google.mail import GoogleMailService
from services.google.oauth import GoogleOAuthService
from services.mail.transformers import MailTransformer
from services.mail.transformers.mail_info import MailInfoTransformer
from services.pipeline.flow.seek_au import SeekAuPipeline

mails_router = APIRouter(
    prefix="/mails",
    tags=["Mail"],
)


@mails_router.post("/list")
async def list_mails(
    request: ListMailsRequestDto,
    token_data: TokenData = Depends(JwtBearer(TokenData)),
):
    user_id = token_data.sub
    oauth_credentials = GoogleOAuthService().get_oauth_credentials(user_id=user_id)

    (thread_infos, next_page_token, total_count) = GoogleMailService().list_threads(
        credentials=oauth_credentials,
        next_page_token=request.next_page_token,
    )
    mail_infos = [
        MailInfoTransformer().transform(data=thread_info)
        for thread_info in thread_infos
    ]

    return ListMailInfosResponseDto(
        mail_infos=mail_infos,
        next_page_token=next_page_token,
        total_count=total_count,
    ).response()


@mails_router.get("/{thread_id}")
async def get_mail(
    thread_id: str, token_data: TokenData = Depends(JwtBearer(TokenData))
):
    user_id = token_data.sub
    oauth_credentials = GoogleOAuthService().get_oauth_credentials(user_id=user_id)
    thread = GoogleMailService().get_thread(
        credentials=oauth_credentials, thread_id=thread_id
    )
    mail = MailTransformer().transform(data=thread)
    return GetMailResponseDto(mail=mail).response()


@mails_router.post("/fitting_by_ai/{thread_id}")
async def mail_fitting_by_ai(
    thread_id: str,
    request: Request,
    token_data: TokenData = Depends(JwtBearer(TokenData)),
):
    user_id = token_data.sub
    json_data = await request.json()
    restriction = json_data["restriction"]
    resume = json_data["resume"]

    oauth_credentials = GoogleOAuthService().get_oauth_credentials(user_id=user_id)
    thread = GoogleMailService().get_thread(
        credentials=oauth_credentials, thread_id=thread_id
    )
    pipeline = SeekAuPipeline()
    result = pipeline.execute()(
        {
            "thread": thread,
            "executor_id": user_id,
            "restriction": restriction,
            "resume": resume,
        }
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


@mails_router.post("/{thread_id}/read")
async def mark_thread_read(
    thread_id: str,
    token_data: TokenData = Depends(JwtBearer(TokenData)),
):
    user_id = token_data.sub
    oauth_credentials = GoogleOAuthService().get_oauth_credentials(user_id=user_id)
    GoogleMailService().mark_thread_read(
        credentials=oauth_credentials,
        thread_id=thread_id,
    )
    return JSONResponse(content={"status": "success"})
