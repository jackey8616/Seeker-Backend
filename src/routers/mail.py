from fastapi import APIRouter, Depends

from dtos.auth.token import TokenData
from dtos.responses.mail.get_mail import GetMailResponseDto
from dtos.responses.mail.list_mails import ListMailInfosResponseDto
from services.auth.auth_bearer import JwtBearer
from services.google.mail import GoogleMailService
from services.google.oauth import GoogleOAuthService
from transformers.mail import MailTransformer
from transformers.mail.mail_info import MailInfoTransformer

mails_router = APIRouter(
    prefix="/mails",
    tags=["Mail"],
)


@mails_router.get("/list")
async def list_mails(token_data: TokenData = Depends(JwtBearer(TokenData))):
    user_id = token_data.sub
    oauth_credentials = GoogleOAuthService().get_oauth_credentials(user_id=user_id)

    (thread_infos, next_page_token) = GoogleMailService().list_threads(
        credentials=oauth_credentials
    )
    mail_infos = [
        MailInfoTransformer().transform(data=thread_info)
        for thread_info in thread_infos
    ]

    return ListMailInfosResponseDto(
        mail_infos=mail_infos,
        next_page_token=next_page_token,
    ).response()


@mails_router.get("/{thread_id}")
async def get_mail(thread_id, token_data: TokenData = Depends(JwtBearer(TokenData))):
    user_id = token_data.sub
    oauth_credentials = GoogleOAuthService().get_oauth_credentials(user_id=user_id)
    thread = GoogleMailService().get_thread(
        credentials=oauth_credentials, thread_id=thread_id
    )
    mail = MailTransformer().transform(data=thread)
    return GetMailResponseDto(mail=mail).response()
