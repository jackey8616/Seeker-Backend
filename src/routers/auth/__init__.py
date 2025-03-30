from fastapi import APIRouter, HTTPException, Request
from kink import di

from responses.auth.refresh import RefreshResponseDto
from services.auth import AuthService

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@auth_router.post("/refresh")
async def refresh(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    service = di[AuthService]
    (access_token, refresh_token, refresh_token_expiration) = service.jwt_refresh(
        token=refresh_token
    )

    response = RefreshResponseDto(access_token=access_token).response()
    response.set_cookie(
        **service.get_refresh_token_cookie_config(
            refresh_token=refresh_token,
            refresh_token_expiration=refresh_token_expiration,
        )
    )
    return response
