from dataclasses import dataclass

from responses.api_response import ApiResponseDto
from services.mail.dtos import Mail


@dataclass
class GetMailResponseDto(ApiResponseDto):
    mail: Mail

    @property
    def data(self):
        return {"mail": self.mail}
