from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from services.ai.quota.exceptions import ExecutionQuotaExceedError


class QuotaErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except ExecutionQuotaExceedError as e:
            return JSONResponse(
                status_code=429,
                content=jsonable_encoder(
                    {
                        "name": e.name,
                        "quotas": e.remaining_quotas,
                    }
                ),
            )
