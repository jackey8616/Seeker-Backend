from os import getenv

from dotenv import load_dotenv
from kink import di

from services.auth import AuthService
from services.google.oauth import GoogleOAuthService
from services.user import UserService


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
    maximum_ai_chat_record_limit = getenv("MAXIMUM_AI_CHAT_RECORD_LIMIT")
    if maximum_ai_chat_record_limit is None:
        raise RuntimeError("MAXIMUM_AI_CHAT_RECORD_LIMIT is not set")
    di["MAXIMUM_AI_CHAT_RECORD_LIMIT"] = int(maximum_ai_chat_record_limit)

    ai_quota_hourly_limit = getenv("AI_QUOTA_HOURLY_LIMIT")
    if ai_quota_hourly_limit is None:
        raise RuntimeError("AI_QUOTA_HOURLY_LIMIT is not set")
    di["AI_QUOTA_HOURLY_LIMIT"] = int(ai_quota_hourly_limit)

    ai_quota_daily_limit = getenv("AI_QUOTA_DAILY_LIMIT")
    if ai_quota_daily_limit is None:
        raise RuntimeError("AI_QUOTA_DAILY_LIMIT is not set")
    di["AI_QUOTA_DAILY_LIMIT"] = int(ai_quota_daily_limit)

    ai_quota_monthly_limit = getenv("AI_QUOTA_MONTHLY_LIMIT")
    if ai_quota_monthly_limit is None:
        raise RuntimeError("AI_QUOTA_MONTHLY_LIMIT is not set")
    di["AI_QUOTA_MONTHLY_LIMIT"] = int(ai_quota_monthly_limit)

    di[UserService] = UserService()
    di[GoogleOAuthService] = GoogleOAuthService()
    di[AuthService] = AuthService()
