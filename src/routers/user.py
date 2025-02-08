from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from kink import di

from dtos.auth.token import TokenData
from dtos.user.userinfo import Userinfo
from repository.user import UserRepository
from services.auth.auth_bearer import JwtBearer

users_router = APIRouter(
    prefix="/users",
    tags=["User"],
)


@users_router.get("/info")
async def info(token_data: TokenData = Depends(JwtBearer(TokenData))):
    user_id = token_data.sub
    repository = di[UserRepository]
    user = repository.get_by_id(id=user_id)
    if user is None:
        userinfo = {}
    else:
        userinfo = Userinfo(name=user.google_userinfo.name)
    return JSONResponse(content=jsonable_encoder(userinfo))
