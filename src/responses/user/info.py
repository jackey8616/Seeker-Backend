from dataclasses import dataclass
from typing import Optional

from responses.api_response import ApiResponseDto
from services.auth.dtos.userinfo import Userinfo


@dataclass
class GetUserInfoResponseDto(ApiResponseDto):
    userinfo: Optional[Userinfo]

    @property
    def data(self):
        return {"userinfo": self.userinfo}
