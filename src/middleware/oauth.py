from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from services.google.oauth.exceptions import OAuthExpiredError, OAuthScopeChangedError


class OAuthErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except OAuthExpiredError as e:
            return JSONResponse(
                status_code=401,
                content={
                    "error": "oauth_expired",
                    "message": str(e),
                    "requires_action": "reauthenticate",
                },
            )
        except OAuthScopeChangedError as e:
            return JSONResponse(
                status_code=401,
                content={
                    "error": "oauth_scope_changed",
                    "message": str(e),
                    "requires_action": "reauthorize",
                },
            )
