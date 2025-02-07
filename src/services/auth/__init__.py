from dataclasses import dataclass, field
from datetime import datetime

from kink import di

from models.user import User
from repository.user import UserRepository
from services.auth.jwt import JwtService
from services.google.oauth import GoogleOAuthService
from utils.time import time_diff_in_seconds


@dataclass
class AuthService:
    _google_oauth_service: GoogleOAuthService = field(
        default_factory=lambda: di[GoogleOAuthService]
    )
    _user_repository: UserRepository = field(default_factory=lambda: di[UserRepository])
    _jwt_service: JwtService = field(default_factory=lambda: JwtService())

    def oauth_login(
        self, code: str, redirect_uri: str
    ) -> tuple[str, str, str, datetime]:
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
            user = self._user_repository.insert_one(
                user=User(
                    google_userinfo=userinfo,
                    google_credentials=credentials,
                )
            )

        assert user.id is not None
        payload = {"sub": user.id}
        (access_token, _) = self._jwt_service.create_access_token(data=payload)
        (refresh_token, refresh_token_expiration) = (
            self._jwt_service.create_refresh_token(data=payload)
        )
        return (user.id, access_token, refresh_token, refresh_token_expiration)

    def jwt_refresh(self, token: str) -> tuple[str, str, datetime]:
        payload = self._jwt_service.decode_token(token=token)
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
            "domain": "localhost",
            "max_age": time_diff_in_seconds(datetime.now(), refresh_token_expiration),
        }
