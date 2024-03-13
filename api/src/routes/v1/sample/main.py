from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Query

from src.common.db import prisma

router = APIRouter(
    prefix="/sample",
    tags=["sample"],
)


@router.get("/users/:user_id")
async def read_user_me(
    user_id: Annotated[
        str, Query(max_length=50, min_length=1, regex="^[a-zA-Z0-9_-]+$")
    ]
):
    return await prisma.user.find_unique(where={"id": user_id})
