from typing import Optional, Sequence

from pydantic import BaseModel

from dtos.repository.order_by import OrderBy
from dtos.repository.paginator import Paginator
from models import MongoDocument


class Cursor(BaseModel):
    previous_page_token: Optional[str]
    next_page_token: Optional[str]

    @staticmethod
    def from_paginator(paginator: Paginator, sorted_results: Sequence[MongoDocument]):
        if len(sorted_results) == 0:
            return Cursor(
                previous_page_token=None,
                next_page_token=None,
            )

        has_more = len(sorted_results) > paginator.n
        first_id = sorted_results[0].id
        last_id = sorted_results[len(sorted_results) - 1].id
        assert first_id is not None
        assert last_id is not None

        return Cursor(
            previous_page_token=Paginator(
                order_by=OrderBy.ASC,
                n=paginator.n,
                start_id=first_id,
            ).encode(),
            next_page_token=Paginator(
                order_by=OrderBy.DESC,
                n=paginator.n,
                start_id=last_id,
            ).encode()
            if has_more
            else None,
        )
