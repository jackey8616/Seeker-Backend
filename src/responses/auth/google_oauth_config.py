from dataclasses import dataclass

from responses.api_response import ApiResponseDto


@dataclass
class GoogleOAuthConfigResponseDto(ApiResponseDto):
    client_id: str
    redirect_uri: str
    scopes: list[str]

    @property
    def data(self):
        return {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scopes": self.scopes,
        }
