from __future__ import annotations

from pydantic import BaseModel, Field

__all__ = ['BookBasisListQueryParams']


class BookBasisListQueryParams(BaseModel):
    """GET list `book-bases/`."""

    only_available: bool | None = Field(None, alias='onlyAvailable')

    model_config = {'populate_by_name': True}
