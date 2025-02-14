from dataclasses import dataclass
from re import findall
from typing import Optional
from urllib.parse import urljoin, urlparse

from dtos.google.mail import GmailMessage, GmailPart, GmailThread
from services.pipeline.step import FinalStep, NextStep, Step, StepDataType


class ExtractLinkFromMailDataType(StepDataType):
    thread: GmailThread


@dataclass
class ExtractLinkFromMailStep(Step[ExtractLinkFromMailDataType]):
    def perform(
        self, data: ExtractLinkFromMailDataType, next: NextStep, final: FinalStep
    ):
        thread = data.thread

        plain_text_part = self._get_plain_text_part(messages=thread.messages)
        if plain_text_part is None:
            return final(
                ValueError("Could not found text/plain message from gmail thread.")
            )

        if plain_text_part.body.decoded_data is None:
            return final(ValueError("Empty part decoded_data"))
        links = self._extract_links(data=plain_text_part.body.decoded_data)

        pass_data = data.model_dump() | {
            "links": links,
        }
        return next(pass_data)

    def _get_plain_text_part(self, messages: list[GmailMessage]) -> Optional[GmailPart]:
        for message in messages:
            for part in message.payload.parts:
                if part.mime_type == "text/plain":
                    return part
        return None

    def _extract_links(self, data: str) -> list[str]:
        links = findall(r"\[(.*?)\]", data)
        filtered_links = list(
            filter(lambda link: "https://www.seek.com.au/job/" in link, links)
        )
        cleaned_links = [urljoin(link, urlparse(link).path) for link in filtered_links]
        return list(set(cleaned_links))
