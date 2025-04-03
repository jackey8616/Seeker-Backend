from fastapi import APIRouter, Depends
from kink import di

from responses.user.info import GetUserInfoResponseDto
from services.auth.auth_bearer import JwtBearer
from services.auth.dtos.token import TokenData
from services.user import UserService

users_router = APIRouter(
    prefix="/users",
    tags=["User"],
)


@users_router.get(
    path="/info",
    response_model=GetUserInfoResponseDto,
)
async def info(
    token_data: TokenData = Depends(JwtBearer(TokenData)),
    user_service: UserService = Depends(lambda: di[UserService]),
):
    user_id = token_data.sub
    userinfo = user_service.get_user_info(user_id=user_id)
    return GetUserInfoResponseDto(userinfo=userinfo).response()
