from services.google.mail.dtos import GmailThreadInfo
from services.mail.dtos.main_info import MailInfo


class MailInfoTransformer:
    def transform(self, data: GmailThreadInfo) -> MailInfo:
        return MailInfo(
            id=data.id,
            snippet=data.snippet,
        )
