from os import getenv

from dotenv import load_dotenv
from kink import di

from repository.user import UserRepository
from services.auth import AuthService
from services.google.oauth import GoogleOAuthService


def bootstrap_di(dotenv_path: str = ".env"):
    load_dotenv(dotenv_path=dotenv_path, override=True)
    di["PORT"] = getenv("PORT")
    di["SSL_KEY_FILE_PATH"] = getenv("SSL_KEY_FILE_PATH")
    di["SSL_CERT_FILE_PATH"] = getenv("SSL_CERT_FILE_PATH")
    di["JWT_SECRET"] = getenv("JWT_SECRET")
    di["SERVE_DOMAIN"] = getenv("SERVE_DOMAIN")
    di["MONGODB_ENDPOINT"] = getenv("MONGODB_ENDPOINT")
    di["MONGODB_DATABASE"] = getenv("MONGODB_DATABASE")
    di["GOOGLE_OAUTH_CLIENT_CREDENTIALS_PATH"] = getenv(
        "GOOGLE_OAUTH_CLIENT_CREDENTIALS_PATH"
    )
    di["GOOGLE_GCP_PROJECT_ID"] = getenv("GOOGLE_GCP_PROJECT_ID")
    di["GOOGLE_GCP_REGION"] = getenv("GOOGLE_GCP_REGION")

    di[UserRepository] = UserRepository()
    di[GoogleOAuthService] = GoogleOAuthService()
    di[AuthService] = AuthService()
