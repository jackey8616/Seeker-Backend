from fastapi import APIRouter, Depends

from dtos.auth.auth_dtos import TokenData
from responses.conversation_log.get_conversation_log import (
    GetConversationLogResponseDto,
)
from responses.conversation_log.get_conversation_logs import (
    GetConversationLogsResponseDto,
)
from services.ai.ai_log_service import AiLogService
from services.auth.auth_bearer import JwtBearer

conversation_log_router = APIRouter(
    prefix="/conversation_logs",
    tags=["ConversationLog"],
)


@conversation_log_router.post(
    path="",
    response_model=GetConversationLogsResponseDto,
)
async def get_conversation_logs(
    paginator_token: str | None = None,
    token_data: TokenData = Depends(JwtBearer(TokenData)),
    ai_log_service: AiLogService = Depends(lambda: AiLogService()),
):
    user_id = token_data.sub
    logs, cursor = ai_log_service.get_many_conversation_log_by_executor_id(
        executor_id=user_id,
        paginator_token=paginator_token,
    )
    return GetConversationLogsResponseDto(logs=logs, cursor=cursor).response()


@conversation_log_router.get(
    path="/{log_id}",
    response_model=GetConversationLogResponseDto,
)
async def get_conversation_log(
    log_id: str,
    token_data: TokenData = Depends(JwtBearer(TokenData)),
    ai_log_service: AiLogService = Depends(lambda: AiLogService()),
):
    user_id = token_data.sub
    log = ai_log_service.get_conversation_log_by_executor_id_and_id(
        id=log_id, executor_id=user_id
    )
    return GetConversationLogResponseDto(log=log).response()
