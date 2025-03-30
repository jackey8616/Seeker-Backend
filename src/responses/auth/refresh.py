from dataclasses import dataclass

from responses.api_response import ApiResponseDto


@dataclass
class RefreshResponseDto(ApiResponseDto):
    access_token: str

    @property
    def data(self):
        return {"access_token": self.access_token}
