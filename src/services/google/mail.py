from base64 import urlsafe_b64decode
from dataclasses import dataclass
from typing import Optional

from googleapiclient.discovery import build

from dtos.google.mail import GmailLabel, GmailThread, GmailThreadInfo
from utils.typings import GoogleOAuthCredentials


@dataclass
class GoogleMailService:
    _default_max_results: int = 10

    def _build_service(self, credentials: GoogleOAuthCredentials):
        return build(serviceName="gmail", version="v1", credentials=credentials)

    def get_seeker_label_id(
        self, credentials: GoogleOAuthCredentials
    ) -> Optional[GmailLabel]:
        service = self._build_service(credentials=credentials)
        raw_labels = (
            service.users().labels().list(userId="me").execute().get("labels", [])
        )
        for raw_label in raw_labels:
            label = GmailLabel.model_validate(raw_label)
            if label.name == "Seeker":
                return label
        return None

    def list_threads(
        self,
        credentials: GoogleOAuthCredentials,
        next_page_token: Optional[str] = None,
    ) -> tuple[list[GmailThreadInfo], Optional[str], int]:
        label = self.get_seeker_label_id(credentials=credentials)
        if label is None:
            raise ValueError("User not apply Seeker label with mail filter")

        service = self._build_service(credentials=credentials)
        thread_result = (
            service.users()
            .threads()
            .list(
                userId="me",
                q="is:unread",
                labelIds=[label.id],
                pageToken=next_page_token,
                maxResults=self._default_max_results,
            )
            .execute()
        )
        next_page_token = thread_result.get("nextPageToken")
        raw_threads = thread_result.get("threads", [])
        threads: list[GmailThreadInfo] = [
            GmailThreadInfo.model_validate(raw_thread) for raw_thread in raw_threads
        ]
        total_count = thread_result.get("resultSizeEstimate", 0)
        return (threads, next_page_token, total_count)

    def get_thread(
        self, credentials: GoogleOAuthCredentials, thread_id: str
    ) -> GmailThread:
        service = self._build_service(credentials=credentials)
        raw_thread = service.users().threads().get(userId="me", id=thread_id).execute()
        actual_thread = GmailThread.model_validate(raw_thread)
        for message in actual_thread.messages:
            parts = message.payload.parts
            if len(parts) == 0:
                continue

            for part in parts:
                if part.body.size == 0 or part.body.data is None:
                    continue

                decoded_bytes = urlsafe_b64decode(part.body.data)
                part.body.decoded_data = decoded_bytes.decode("utf-8")
        return actual_thread
