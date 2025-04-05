from dataclasses import dataclass

from dtos.mail.mail_dtos import Mail
from responses.api_response import ApiResponseDto


@dataclass
class GetMailResponseDto(ApiResponseDto):
    mail: Mail

    @property
    def data(self):
        return {"mail": self.mail}
