from dataclasses import dataclass, field
from datetime import datetime
from urllib.parse import urlparse

from kink import di

from dtos.auth.auth_dtos import TokenData
from dtos.google.oauth_dtos import GoogleCredentials, GoogleUserInfo
from models.user.user import ModelUser
from repository.user import UserRepository
from services.auth.jwt import JwtService
from services.google.oauth import GoogleOAuthService
from utils.time import time_diff_in_seconds


@dataclass
class AuthService:
    _google_oauth_service: GoogleOAuthService = field(
        default_factory=lambda: di[GoogleOAuthService]
    )
    _jwt_service: JwtService = field(default_factory=lambda: JwtService())
    _user_repository: UserRepository = field(default_factory=lambda: UserRepository())

    def oauth_login(self, code: str, redirect_uri: str) -> tuple[str, str, datetime]:
        (oauth_credentials, credentials) = (
            self._google_oauth_service.exchange_oauth_token(
                code=code, redirect_uri=redirect_uri
            )
        )
        userinfo = self._google_oauth_service.get_userinfo(
            credentials=oauth_credentials
        )

        user = self._user_repository.get_by_google_id(google_id=userinfo.id)
        if user is None:
            user = self._create_new_user_through_oauth(
                userinfo=userinfo,
                credentials=credentials,
            )
        else:
            user.google_credentials = credentials
            self._user_repository.update(obj=user)

        assert user.id is not None
        payload = TokenData(sub=user.id)
        (access_token, _) = self._jwt_service.create_access_token(
            data=payload.model_dump()
        )
        (refresh_token, refresh_token_expiration) = (
            self._jwt_service.create_refresh_token(data=payload.model_dump())
        )
        return (access_token, refresh_token, refresh_token_expiration)

    def jwt_refresh(self, token: str) -> tuple[str, str, datetime]:
        payload = self._jwt_service.decode_token(token=token)
        if isinstance(payload, Exception):
            raise payload

        user_id = payload["sub"]
        if user_id is None:
            raise ValueError("Incorrect payload")

        (access_token, _) = self._jwt_service.create_access_token(data=payload)
        (refresh_token, refresh_token_expiration) = (
            self._jwt_service.create_refresh_token(data=payload)
        )
        return (access_token, refresh_token, refresh_token_expiration)

    def get_refresh_token_cookie_config(
        self, refresh_token: str, refresh_token_expiration: datetime
    ) -> dict:
        return {
            "key": "refresh_token",
            "value": refresh_token,
            "httponly": True,
            "secure": True,
            "samesite": "none",
            "domain": urlparse(di["SERVE_DOMAIN"]).hostname,
            "max_age": time_diff_in_seconds(datetime.now(), refresh_token_expiration),
        }

    def _create_new_user_through_oauth(
        self, userinfo: GoogleUserInfo, credentials: GoogleCredentials
    ) -> ModelUser:
        return self._user_repository.insert_one(
            obj=ModelUser(
                google_userinfo=userinfo,
                google_credentials=credentials,
            )
        )
