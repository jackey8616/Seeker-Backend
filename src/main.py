from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from bootstrap import bootstrap_di
from middleware.oauth import OAuthErrorMiddleware
from middleware.quota import QuotaErrorMiddleware
from routers.auth import auth_router
from routers.auth.oauth import oauth_router
from routers.conversation_log import conversation_log_router
from routers.job import jobs_router
from routers.mail import mails_router
from routers.user import users_router
from utils.logger import setup_log


def create_app(title: str = "Seeker-Backend") -> FastAPI:
    origins = [
        "https://localhost:8080",
        "https://localhost:5173",
        "https://seeker.clo5de.info",
        "https://seeker-backend.clo5de.info",
    ]
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(OAuthErrorMiddleware),
        Middleware(QuotaErrorMiddleware),
    ]

    app = FastAPI(title=title, middleware=middleware)
    auth_router.include_router(router=oauth_router)
    app.include_router(router=auth_router)
    app.include_router(router=users_router)
    app.include_router(router=mails_router)
    app.include_router(router=conversation_log_router)
    app.include_router(router=jobs_router)

    return app


if __name__ == "__main__":
    from argparse import ArgumentParser

    from kink import di
    from uvicorn import run

    from bootstrap import bootstrap_di

    setup_log()
    parser = ArgumentParser()
    parser.add_argument("--env-file-path", type=str, required=True)
    args = parser.parse_args()
    env_file_path = args.env_file_path

    bootstrap_di(dotenv_path=env_file_path)
    run(
        app=create_app(),
        host="0.0.0.0",
        port=int(di["PORT"]),
        ssl_keyfile=di["SSL_KEY_FILE_PATH"],
        ssl_certfile=di["SSL_CERT_FILE_PATH"],
    )
