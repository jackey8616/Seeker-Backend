from typing import Optional

from pydantic import BaseModel, Field


class GmailBody(BaseModel):
    size: int
    data: Optional[str] = None
    decoded_data: Optional[str] = None


class GmailPayloadBody(GmailBody):
    attachment_id: Optional[str] = Field(alias="attachmentId", default=None)


class GmailHeader(BaseModel):
    name: str
    value: str


class GmailPart(BaseModel):
    part_id: str = Field(alias="partId")
    mime_type: str = Field(alias="mimeType")
    filename: str
    headers: list[GmailHeader]
    body: GmailBody


class GmailPayload(BaseModel):
    body: GmailPayloadBody
    filename: str
    headers: list[GmailHeader]
    mime_type: str = Field(alias="mimeType")
    partId: str
    parts: list[GmailPart]


class GmailMessage(BaseModel):
    history_id: str = Field(alias="historyId")
    id: str
    internal_date: str = Field(alias="internalDate")
    label_ids: list[str] = Field(alias="labelIds")
    payload: GmailPayload
    snippet: str
    size_estimate: int = Field(alias="sizeEstimate")
    raw: Optional[str] = None
    thread_id: str = Field(alias="threadId")


class GmailThreadInfo(BaseModel):
    id: str
    history_id: str = Field(alias="historyId")
    snippet: str


class GmailThread(GmailThreadInfo):
    messages: list[GmailMessage]
    snippet: Optional[str] = None


class GmailLabel(BaseModel):
    id: str
    name: str
    type: str
