from dtos.google.mail_dtos import GmailThreadInfo
from dtos.mail.mail_dtos import MailInfo


class MailInfoTransformer:
    def transform(self, data: GmailThreadInfo) -> MailInfo:
        return MailInfo(
            id=data.id,
            snippet=data.snippet,
        )
