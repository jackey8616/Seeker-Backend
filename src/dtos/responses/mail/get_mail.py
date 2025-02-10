from dataclasses import dataclass

from dtos.mail import Mail
from dtos.responses.api_response import ApiResponseDto


@dataclass
class GetMailResponseDto(ApiResponseDto):
    mail: Mail

    @property
    def data(self):
        return {"mail": self.mail}
