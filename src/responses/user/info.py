from dataclasses import dataclass
from typing import Optional

from dtos.auth.auth_dtos import Userinfo
from responses.api_response import ApiResponseDto


@dataclass
class GetUserInfoResponseDto(ApiResponseDto):
    userinfo: Optional[Userinfo]

    @property
    def data(self):
        return {"userinfo": self.userinfo}
