from dtos.google.mail import GmailThreadInfo
from dtos.mail.main_info import MailInfo


class MailInfoTransformer:
    def transform(self, data: GmailThreadInfo) -> MailInfo:
        return MailInfo(
            id=data.id,
            snippet=data.snippet,
        )
