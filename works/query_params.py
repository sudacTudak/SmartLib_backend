from __future__ import annotations

from pydantic import BaseModel, Field

__all__ = ['WorkListQueryParams']


class WorkListQueryParams(BaseModel):
    """GET list `works/`."""

    only_available: bool | None = Field(None, alias='onlyAvailable')
    category: str | None = Field(None, alias='category')

    model_config = {'populate_by_name': True}

