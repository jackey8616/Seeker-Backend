from typing import Optional, Type, TypeVar

from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import ExpiredSignatureError, InvalidTokenError
from pydantic import BaseModel

from services.auth.jwt import JwtService

T = TypeVar("T", bound=BaseModel)


class JwtBearer(HTTPBearer):
    def __init__(self, model: Type[T], auto_error: bool = True):
        super().__init__(auto_error=auto_error)
        self._model = model

    async def __call__(self, request: Request):
        credentials: Optional[HTTPAuthorizationCredentials] = await super().__call__(
            request
        )
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )

            decoded_payload = JwtService().decode_token(token=credentials.credentials)
            if isinstance(decoded_payload, ExpiredSignatureError):
                raise HTTPException(status_code=401, detail="Expired token.")
            elif isinstance(decoded_payload, InvalidTokenError):
                raise HTTPException(status_code=403, detail="Invalid token.")
            elif isinstance(decoded_payload, Exception):
                raise HTTPException(
                    status_code=401, detail="Unknown verification exception"
                )

            return self._model.model_validate(decoded_payload)
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")
