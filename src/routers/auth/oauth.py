from fastapi import APIRouter, Request
from kink import di

from responses.auth.google_oauth_config import GoogleOAuthConfigResponseDto
from responses.auth.google_oauth_url import GoogleOAuthUrlResponseDto
from responses.auth.google_oauth_verify import GoogleOAuthVerifyResponseDto
from services.auth import AuthService
from services.google.oauth import GoogleOAuthService

oauth_router = APIRouter(
    prefix="/oauth",
    tags=["Auth"],
)


@oauth_router.get("/google/config")
async def get_google_config():
    service: GoogleOAuthService = di[GoogleOAuthService]
    client_id, scopes = service.get_oauth_config()
    return GoogleOAuthConfigResponseDto(
        client_id=client_id,
        redirect_uri=di["SERVE_DOMAIN"],
        scopes=scopes,
    ).response()


@oauth_router.get("/google/url", response_model=GoogleOAuthUrlResponseDto)
async def get_google_oauth_url():
    service: GoogleOAuthService = di[GoogleOAuthService]
    url, state = service.get_oauth_url(redirect_uri=di["SERVE_DOMAIN"])
    return GoogleOAuthUrlResponseDto(url=url).response()


@oauth_router.post("/google/verify")
async def google_oauth_code_verify(request: Request):
    json_data = await request.json()
    code = json_data["code"]

    service = di[AuthService]
    (access_token, refresh_token, refresh_token_expiration) = service.oauth_login(
        code=code,
        redirect_uri=di["SERVE_DOMAIN"],
    )

    response = GoogleOAuthVerifyResponseDto(access_token=access_token).response()
    response.set_cookie(
        **service.get_refresh_token_cookie_config(
            refresh_token=refresh_token,
            refresh_token_expiration=refresh_token_expiration,
        )
    )
    return response
