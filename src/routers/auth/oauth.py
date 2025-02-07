from fastapi import APIRouter, Request
from kink import di

from dtos.responses.auth.google_oauth_config import GoogleOAuthConfigResponseDto
from dtos.responses.auth.google_oauth_url import GoogleOAuthUrlResponseDto
from dtos.responses.auth.google_oauth_verify import GoogleOAuthVerifyResponseDto
from services.auth import AuthService
from services.google.oauth import GoogleOAuthService

oauth_router = APIRouter(
    prefix="/oauth",
    tags=["Auth"],
)


def get_verify_path():
    serve_domain = di["SERVE_DOMAIN"]
    return serve_domain


@oauth_router.get("/google/config")
async def get_google_config():
    service: GoogleOAuthService = di[GoogleOAuthService]
    redirect_uri = get_verify_path()
    client_id, scopes = service.get_oauth_config()
    return GoogleOAuthConfigResponseDto(
        client_id=client_id,
        redirect_uri=redirect_uri,
        scopes=scopes,
    ).response()


@oauth_router.get("/google/url", response_model=GoogleOAuthUrlResponseDto)
async def get_google_oauth_url():
    service: GoogleOAuthService = di[GoogleOAuthService]
    url, state = service.get_oauth_url(redirect_uri=get_verify_path())
    return GoogleOAuthUrlResponseDto(url=url).response()


@oauth_router.post("/google/verify")
async def google_oauth_code_verify(request: Request):
    json_data = await request.json()
    code = json_data["code"]

    service = di[AuthService]
    (user_id, access_token, refresh_token, refresh_token_expiration) = (
        service.oauth_login(
            code=code,
            redirect_uri=get_verify_path(),
        )
    )

    response = GoogleOAuthVerifyResponseDto(
        user_id=user_id, access_token=access_token
    ).response()
    response.set_cookie(
        **service.get_refresh_token_cookie_config(
            refresh_token=refresh_token,
            refresh_token_expiration=refresh_token_expiration,
        )
    )
    return response
