from os import getenv

from dotenv import load_dotenv
from kink import di

from repository.user import UserRepository
from services.auth import AuthService
from services.google.oauth import GoogleOAuthService


def bootstrap_di(dotenv_path: str = ".env"):
    load_dotenv(dotenv_path=dotenv_path, override=True)
    di["PORT"] = getenv("PORT")
    di["JWT_SECRET"] = getenv("JWT_SECRET")
    di["SERVE_DOMAIN"] = getenv("SERVE_DOMAIN")
    di["MONGODB_ENDPOINT"] = getenv("MONGODB_ENDPOINT")
    di["MONGODB_DATABASE"] = getenv("MONGODB_DATABASE")
    di["GOOGLE_OAUTH_CLIENT_CREDENTIALS_PATH"] = getenv(
        "GOOGLE_OAUTH_CLIENT_CREDENTIALS_PATH"
    )

    di[UserRepository] = UserRepository()
    di[GoogleOAuthService] = GoogleOAuthService()
    di[AuthService] = AuthService()
