from __future__ import annotations

from pydantic import BaseModel, Field, UUID4

from common_core.fields import OptionalListQueryParam
from works.enums import WorkCategory

__all__ = ['WorkListQueryParams', 'WorkSimilarQueryParams']


class WorkListQueryParams(BaseModel):
    """GET list `works/`."""

    search: str | None = Field(None, alias='q')
    popular: bool | None = None
    only_available: bool | None = Field(None, alias='onlyAvailable')
    has_online_version: bool | None = Field(None, alias='hasOnlineVersion')
    category: WorkCategory | None = None
    authors: OptionalListQueryParam[str] = None
    genres: OptionalListQueryParam[str] = None
    library_branches: OptionalListQueryParam[str] = Field(None, alias='libraryBranch')

    model_config = {'populate_by_name': True}


class WorkSimilarQueryParams(BaseModel):
    """GET ``works/similar/``."""

    work_id: UUID4 = Field(..., alias='workId')
    limit: int = Field(12, ge=1, le=50, alias='limit')

    model_config = {'populate_by_name': True}
