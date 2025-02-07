from dataclasses import dataclass

from dtos.responses.api_response import ApiResponseDto


@dataclass
class GoogleOAuthVerifyResponseDto(ApiResponseDto):
    user_id: str
    access_token: str

    @property
    def data(self):
        return {
            "user_id": self.user_id,
            "access_token": self.access_token,
        }
