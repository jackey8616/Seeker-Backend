from dataclasses import dataclass, field
from typing import Optional

from google.auth.exceptions import OAuthError
from google.auth.external_account_authorized_user import Credentials as extCredentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from kink import di

from models.user import ModelUser
from services.google.oauth.dtos.google_credentials import GoogleCredentials
from services.google.oauth.dtos.google_user_info import GoogleUserInfo
from services.google.oauth.exceptions import OAuthExpiredError, OAuthScopeChangedError
from services.google.oauth.transformer import GoogleCredentialsTransformer
from services.user import UserService
from utils.typings import GoogleOAuthCredentials


@dataclass
class GoogleOAuthService:
    _user_service: UserService = field(default_factory=lambda: di[UserService])
    _credential_json_path: str = field(
        default_factory=lambda: di["GOOGLE_OAUTH_CLIENT_CREDENTIALS_PATH"], repr=False
    )
    _seeker_required_scopes: list[str] = field(
        default_factory=lambda: [
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/gmail.readonly",
            "https://www.googleapis.com/auth/gmail.modify",
        ]
    )

    def _build_service(self, credentials: GoogleOAuthCredentials):
        return build(serviceName="oauth2", version="v2", credentials=credentials)

    def _get_oauth_flow(
        self,
        scopes: Optional[list[str]] = None,
        state: Optional[str] = None,
        redirect_uri: Optional[str] = None,
    ) -> Flow:
        payload = {
            "client_secrets_file": self._credential_json_path,
            "scopes": self._seeker_required_scopes if scopes is None else scopes,
        }
        if state is not None:
            payload["state"] = state
        if redirect_uri is not None:
            payload["redirect_uri"] = redirect_uri

        return Flow.from_client_secrets_file(**payload)

    def get_oauth_config(self) -> tuple[str, list[str]]:
        flow = self._get_oauth_flow()
        return (
            flow.client_config["client_id"],
            self._seeker_required_scopes,
        )

    def get_oauth_url(self, redirect_uri: str) -> tuple[str, str]:
        flow = self._get_oauth_flow(redirect_uri=redirect_uri)
        authorization_url, state = flow.authorization_url(
            access_type="offline",
        )
        return (authorization_url, state)

    def exchange_oauth_token(
        self, code: str, redirect_uri: str
    ) -> tuple[GoogleOAuthCredentials, GoogleCredentials]:
        flow = self._get_oauth_flow(redirect_uri=redirect_uri)
        try:
            flow.fetch_token(code=code)
            return (
                flow.credentials,
                GoogleCredentialsTransformer().transform(data=flow.credentials),
            )
        except Warning as w:
            if "scope has changed" in str(w).lower():
                raise OAuthScopeChangedError(
                    "The requested scopes have changed. Please re-authorize the application."
                ) from w
            raise

    def refresh_oauth_token(self, user: ModelUser, credentials: extCredentials):
        try:
            credentials.refresh(Request())
            if not self._has_required_scopes(credentials):
                raise OAuthScopeChangedError(
                    "The application requires additional permissions. Please re-authorize."
                )
            user.google_credentials = GoogleCredentialsTransformer().transform(
                data=credentials
            )
            self._user_service.update(user=user)
        except OAuthError as e:
            raise OAuthExpiredError(
                "Google OAuth credentials have expired. Please re-authenticate."
            ) from e
        except OAuthScopeChangedError as e:
            raise e
        except Exception as e:
            raise ValueError(f"Failed to refresh OAuth credentials: {str(e)}") from e

    def get_userinfo(self, credentials: GoogleOAuthCredentials) -> GoogleUserInfo:
        service = self._build_service(credentials=credentials)
        return GoogleUserInfo.model_validate(service.userinfo().get().execute())

    def _has_required_scopes(self, credentials: GoogleOAuthCredentials) -> bool:
        if not hasattr(credentials, "scopes") or credentials.scopes is None:
            return False
        return all(
            scope in credentials.scopes for scope in self._seeker_required_scopes
        )

    def get_oauth_credentials(self, user_id: str) -> GoogleOAuthCredentials:
        user = self._user_service.get_by_id(user_id=user_id)
        if user is None:
            raise ValueError(f"Could not find user with id: {user_id}")
        elif user.google_credentials is None:
            raise ValueError(f"User with id: {user_id} has no Google OAuth credentials")

        flow = self._get_oauth_flow()
        info = {
            "client_id": flow.client_config["client_id"],
            "client_secret": flow.client_config["client_secret"],
            "token_url": flow.client_config["token_uri"],
        } | user.google_credentials.model_dump(mode="json")

        credentials = extCredentials.from_info(info=info)

        if credentials.expired:
            self.refresh_oauth_token(user=user, credentials=credentials)

        return credentials
