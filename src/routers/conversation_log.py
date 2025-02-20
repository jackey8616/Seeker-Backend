from fastapi import APIRouter, Depends

from dtos.auth.token import TokenData
from dtos.responses.conversation_log.get_conversation_log import (
    GetConversationLogResponseDto,
)
from dtos.responses.conversation_log.get_conversation_logs import (
    GetConversationLogsResponseDto,
)
from services.ai_log import AiLogService
from services.auth.auth_bearer import JwtBearer

conversation_log_router = APIRouter(
    prefix="/conversation_logs",
    tags=["ConversationLog"],
)


@conversation_log_router.get(
    path="",
    response_model=GetConversationLogsResponseDto,
)
async def get_conversation_logs(
    token_data: TokenData = Depends(JwtBearer(TokenData)),
    ai_log_service: AiLogService = Depends(lambda: AiLogService()),
):
    user_id = token_data.sub
    logs = ai_log_service.get_many_conversation_log_by_executor_id(executor_id=user_id)
    return GetConversationLogsResponseDto(logs=logs).response()


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
