from email.utils import parsedate_to_datetime

from dtos.google.mail_dtos import GmailThread
from dtos.mail.mail_dtos import Mail


class MailTransformer:
    def transform(self, data: GmailThread) -> Mail:
        first_message = data.messages[0]
        headers = first_message.payload.headers

        title = None
        sender = None
        date = None
        for header in headers:
            match header.name.lower():
                case "subject":
                    title = header.value
                case "from":
                    sender = header.value
                case "date":
                    date = parsedate_to_datetime(header.value)
                case _:
                    pass

        assert title is not None
        assert sender is not None
        assert date is not None

        extracted_data = ""
        for message in data.messages:
            for part in message.payload.parts:
                if part.mime_type != "text/html":
                    continue

                decoded_data = part.body.decoded_data
                if decoded_data is None:
                    continue
                extracted_data = decoded_data

        return Mail(
            id=data.id,
            title=title,
            sender=sender,
            date=date,
            snippet="",
            is_extracted=False,
            extracted_data=extracted_data,
        )
