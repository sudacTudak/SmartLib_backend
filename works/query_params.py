from __future__ import annotations

from pydantic import BaseModel, Field, UUID4

__all__ = ['WorkListQueryParams', 'WorkSimilarQueryParams']


class WorkListQueryParams(BaseModel):
    """GET list `works/`."""

    only_available: bool | None = Field(None, alias='onlyAvailable')
    category: str | None = Field(None, alias='category')

    model_config = {'populate_by_name': True}


class WorkSimilarQueryParams(BaseModel):
    """GET ``works/similar/``."""

    work_id: UUID4 = Field(..., alias='workId')
    limit: int = Field(12, ge=1, le=50, alias='limit')

    model_config = {'populate_by_name': True}

