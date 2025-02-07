from dataclasses import dataclass

from dtos.responses.api_response import ApiResponseDto


@dataclass
class GoogleOAuthUrlResponseDto(ApiResponseDto):
    url: str

    @property
    def data(self):
        return {
            "url": self.url,
        }
