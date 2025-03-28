from dataclasses import dataclass, field
from typing import Optional

from google.auth.external_account_authorized_user import Credentials as extCredentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from kink import di

from dtos.google.credentials import GoogleCredentials
from dtos.google.userinfo import GoogleUserInfo
from repository.user import UserRepository
from transformers.auth.google_credentials import GoogleCredentialsTransformer
from utils.typings import GoogleOAuthCredentials


@dataclass
class GoogleOAuthService:
    _credential_json_path: str = field(
        default_factory=lambda: di["GOOGLE_OAUTH_CLIENT_CREDENTIALS_PATH"], repr=False
    )
    _seeker_required_scopes: list[str] = field(
        default_factory=lambda: [
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/gmail.readonly",
        ]
    )

    def _build_service(self, credentials: GoogleOAuthCredentials):
        return build(serviceName="oauth2", version="v2", credentials=credentials)

    def _get_oauth_flow(
        self, scopes: Optional[list[str]] = None, state: Optional[str] = None
    ) -> Flow:
        payload = {
            "client_secrets_file": self._credential_json_path,
            "scopes": self._seeker_required_scopes if scopes is None else scopes,
        }
        if state is not None:
            payload["state"] = state

        return Flow.from_client_secrets_file(**payload)

    def get_oauth_config(self) -> tuple[str, list[str]]:
        flow = self._get_oauth_flow()
        return (
            flow.client_config["client_id"],
            self._seeker_required_scopes,
        )

    def get_oauth_url(self, redirect_uri: str) -> tuple[str, str]:
        flow = self._get_oauth_flow()
        flow.redirect_uri = redirect_uri
        authorization_url, state = flow.authorization_url(
            access_type="offline",
        )
        return (authorization_url, state)

    def exchange_oauth_token(
        self, code: str, redirect_uri: str
    ) -> tuple[GoogleOAuthCredentials, GoogleCredentials]:
        flow = self._get_oauth_flow()
        flow.redirect_uri = redirect_uri
        flow.fetch_token(code=code)
        return (
            flow.credentials,
            GoogleCredentialsTransformer().transform(data=flow.credentials),
        )

    def get_userinfo(self, credentials: GoogleOAuthCredentials) -> GoogleUserInfo:
        service = self._build_service(credentials=credentials)
        return GoogleUserInfo.model_validate(service.userinfo().get().execute())

    def get_oauth_credentials(self, user_id: str) -> GoogleOAuthCredentials:
        user_repository = di[UserRepository]
        user = user_repository.get_by_id(id=user_id)

        if user is None:
            raise ValueError(f"Could not find user with id: {user_id}")

        flow = self._get_oauth_flow()
        info = {
            "client_id": flow.client_config["client_id"],
            "client_secret": flow.client_config["client_secret"],
            "token_url": flow.client_config["token_uri"],
        } | user.google_credentials.model_dump(mode="json")

        credentials = extCredentials.from_info(info=info)

        if credentials.expired:
            try:
                credentials.refresh(Request())
                user.google_credentials = GoogleCredentialsTransformer().transform(
                    data=credentials
                )
                user_repository.update(user)
            except Exception as e:
                raise ValueError(
                    "Google OAuth credentials have expired. Please re-authenticate."
                ) from e

        return credentials
