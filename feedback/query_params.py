from __future__ import annotations

from pydantic import BaseModel, Field, UUID4

__all__ = [
    'WorkParentQueryParams',
    'WorkByUserQueryParams',
    'LibraryBranchParentQueryParams',
    'LibraryBranchByUserQueryParams',
]


class WorkParentQueryParams(BaseModel):
    work_id: UUID4 | None = Field(None, alias='workId')

    model_config = {'populate_by_name': True}


class WorkByUserQueryParams(WorkParentQueryParams):
    client_id: UUID4 | None = Field(None, alias='clientId')

    model_config = {'populate_by_name': True}


class LibraryBranchParentQueryParams(BaseModel):
    library_branch_id: UUID4 | None = Field(None, alias='libraryBranchId')

    model_config = {'populate_by_name': True}


class LibraryBranchByUserQueryParams(LibraryBranchParentQueryParams):
    client_id: UUID4 | None = Field(None, alias='clientId')

    model_config = {'populate_by_name': True}
