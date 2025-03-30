from datetime import datetime

from services.mail.dtos.main_info import MailInfo


class Mail(MailInfo):
    title: str
    sender: str
    date: datetime
    is_extracted: bool
    extracted_data: str
