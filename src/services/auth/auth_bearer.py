from typing import Optional

from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import ExpiredSignatureError

from services.auth.jwt import JwtService


class JwtBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JwtBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: Optional[HTTPAuthorizationCredentials] = await super(
            JwtBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )

            validate_result = self.verify_jwt(credentials.credentials)
            if isinstance(validate_result, ExpiredSignatureError):
                raise HTTPException(status_code=401, detail="Expired token.")
            elif validate_result is False:
                raise HTTPException(status_code=403, detail="Invalid token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwt_token: str) -> bool | ExpiredSignatureError:
        is_valid = False
        try:
            token = JwtService().decode_token(token=jwt_token)
            if token is not None:
                is_valid = True
        except ExpiredSignatureError as e:
            is_valid = e
        return is_valid
