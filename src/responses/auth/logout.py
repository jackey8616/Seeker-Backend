from dataclasses import dataclass

from responses.api_response import ApiResponseDto


@dataclass
class LogoutResponseDto(ApiResponseDto):
    @property
    def data(self):
        return {}
