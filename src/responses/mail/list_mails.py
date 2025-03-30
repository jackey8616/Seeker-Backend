from dataclasses import dataclass
from typing import Optional

from responses.api_response import ApiResponseDto
from services.mail.dtos.main_info import MailInfo


@dataclass
class ListMailInfosResponseDto(ApiResponseDto):
    mail_infos: list[MailInfo]
    next_page_token: Optional[str]
    total_count: int

    @property
    def data(self):
        return {
            "mail_infos": self.mail_infos,
            "next_page_token": self.next_page_token,
            "total_count": self.total_count,
        }
