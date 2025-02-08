from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Optional

from jwt import decode, encode
from kink import di


@dataclass
class JwtService:
    _algorithm: str = field(default="HS256", repr=False)
    _jwt_secret: str = field(default_factory=lambda: di["JWT_SECRET"], repr=False)
    _access_token_timedelta: timedelta = timedelta(minutes=30)
    _refresh_token_timedelta: timedelta = timedelta(days=30)

    def _create_token(
        self, data: dict, expires_delta: timedelta
    ) -> tuple[str, datetime]:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        return encode(to_encode, self._jwt_secret, algorithm=self._algorithm), expire

    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ) -> tuple[str, datetime]:
        return self._create_token(
            data=data,
            expires_delta=expires_delta
            if expires_delta is not None
            else self._access_token_timedelta,
        )

    def create_refresh_token(self, data: dict) -> tuple[str, datetime]:
        return self._create_token(
            data=data, expires_delta=self._refresh_token_timedelta
        )

    def decode_token(self, token: str) -> dict | Exception:
        try:
            return decode(token, self._jwt_secret, algorithms=[self._algorithm])
        except Exception as e:
            return e
