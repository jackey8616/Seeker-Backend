from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from kink import di

from dtos.user.userinfo import Userinfo
from repository.user import UserRepository
from services.auth.auth_bearer import JwtBearer

users_router = APIRouter(
    prefix="/users",
    tags=["User"],
)


@users_router.get("/info/{userid}", dependencies=[Depends(JwtBearer())])
async def info(userid: str):
    repository = di[UserRepository]
    user = repository.get_by_id(id=userid)
    if user is None:
        userinfo = {}
    else:
        userinfo = Userinfo(name=user.google_userinfo.name)
    return JSONResponse(content=jsonable_encoder(userinfo))
