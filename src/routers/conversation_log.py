from fastapi import APIRouter, Depends

from dtos.auth.token import TokenData
from dtos.responses.conversation_log.get_conversation_log import (
    GetConversationLogResponseDto,
)
from dtos.responses.conversation_log.get_conversation_logs import (
    GetConversationLogsResponseDto,
)
from repository.ai_conversation_log import AiConversationLogRepository
from services.auth.auth_bearer import JwtBearer

conversation_log_router = APIRouter(
    prefix="/conversation_logs",
    tags=["ConversationLog"],
)


@conversation_log_router.get(
    path="",
    response_model=GetConversationLogsResponseDto,
)
async def get_conversation_logs(token_data: TokenData = Depends(JwtBearer(TokenData))):
    user_id = token_data.sub
    logs = AiConversationLogRepository().get_many_by_executor_id(executor_id=user_id)
    return GetConversationLogsResponseDto(logs=logs).response()


@conversation_log_router.get(
    path="/{log_id}",
    response_model=GetConversationLogResponseDto,
)
async def get_conversation_log(
    log_id: str,
    token_data: TokenData = Depends(JwtBearer(TokenData)),
):
    user_id = token_data.sub
    log = AiConversationLogRepository().get_by_executor_id_and_id(
        id=log_id, executor_id=user_id
    )
    return GetConversationLogResponseDto(log=log).response()
