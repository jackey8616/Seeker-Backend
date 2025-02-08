from dataclasses import dataclass

from dtos.responses.api_response import ApiResponseDto


@dataclass
class GoogleOAuthVerifyResponseDto(ApiResponseDto):
    access_token: str

    @property
    def data(self):
        return {
            "access_token": self.access_token,
        }
