from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from kink import di

from services.auth.auth_bearer import JwtBearer
from services.auth.dtos.token import TokenData
from services.auth.dtos.userinfo import Userinfo
from services.user import UserService

users_router = APIRouter(
    prefix="/users",
    tags=["User"],
)


@users_router.get("/info")
async def info(
    token_data: TokenData = Depends(JwtBearer(TokenData)),
    user_service: UserService = Depends(lambda: di[UserService]),
):
    user_id = token_data.sub
    user = user_service.get_by_id(user_id=user_id)
    if user is None:
        userinfo = {}
    else:
        userinfo = Userinfo(name=user.google_userinfo.name)
    return JSONResponse(content=jsonable_encoder(userinfo))
