from __future__ import annotations

from pydantic import BaseModel, Field


class Attachment(BaseModel):
    id: str
    grant_id: str | None = Field(exclude=True, default=None)
    filename: str | None = None
    content_type: str | None = None
    size: int | None = None
    content_id: str | None = None
    content_disposition: str | None = None
    is_inline: bool | None = None


class MessageHeader(BaseModel):
    name: str
    value: str


class EmailName(BaseModel):
    email: str
    name: str | None = None


class Message(BaseModel):
    grant_id: str = Field(..., exclude=True)
    from_: list[EmailName] = Field(alias="from", validation_alias="from_")
    object: str = "message"
    id: str | None = None
    body: str | None = None
    thread_id: str | None = None
    subject: str | None = None
    snippet: str | None = None
    to: list[EmailName] | None = None
    bcc: list[EmailName] | None = None
    cc: list[EmailName] | None = None
    reply_to: list[EmailName] | None = None
    attachments: list[Attachment] | None = None
    folders: list[str] | None = None
    headers: list[MessageHeader] | None = None
    unread: bool | None = None
    starred: bool | None = None
    created_at: int | None = None
    date: int | None = None


class MessageListResponse(BaseModel):
    request_id: str
    data: list[Message]
    next_cursor: str | None = None


class MessagePreview(BaseModel):
    id: str | None = None
    from_: list[EmailName] = Field(alias="from", validation_alias="from_")
    subject: str | None = None
    snippet: str | None = None
    has_attachments: bool = False
    created_at: int | None = None
