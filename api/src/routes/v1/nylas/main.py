from __future__ import annotations

from fastapi import APIRouter, HTTPException

from src.common.db import prisma
from src.common.nylas import nylas_client
from src.models.nylas import MessagePreview

router = APIRouter(
    prefix="/nylas",
    tags=["nylas"],
)


@router.get("/messages", response_model=list[MessagePreview])
async def nylas_messages_list():
    # first we need to get the grant id from our user id
    user = await prisma.user.find_unique(
        where={"email": "shaun@shaunberryman.com"},
        include={"nylas_accounts": True},
    )

    # ensure we have a grant id
    # also need to check and see if it has been deleted, etc.
    if not user.nylas_accounts or len(user.nylas_accounts) < 1:
        raise HTTPException(status_code=404, detail="No nylas grant id found")

    # get the grant id
    grant_id = user.nylas_accounts[0].grant_id

    # get the messages
    messages = nylas_client.messages.list(
        grant_id, query_params={"limit": 10, "unread": "true"}
    )

    # map our messages to the response model
    result = [
        MessagePreview(
            id=message.id,
            from_=message.from_,
            subject=message.subject,
            snippet=message.snippet,
            has_attachments=message.attachments is not None
            and len(message.attachments) > 0,
            created_at=message.created_at if message.created_at else message.date,
        )
        for message in messages.data
    ]

    return result
