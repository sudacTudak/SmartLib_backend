from __future__ import annotations

from pydantic import BaseModel, Field, UUID4

__all__ = [
    'BookBasisParentQueryParams',
    'BookBasisByUserQueryParams',
    'LibraryBranchParentQueryParams',
    'LibraryBranchByUserQueryParams',
]


class BookBasisParentQueryParams(BaseModel):
    book_basis_id: UUID4 | None = Field(None, alias='bookBasisId')

    model_config = {'populate_by_name': True}


class BookBasisByUserQueryParams(BookBasisParentQueryParams):
    client_id: UUID4 | None = Field(None, alias='clientId')

    model_config = {'populate_by_name': True}


class LibraryBranchParentQueryParams(BaseModel):
    library_branch_id: UUID4 | None = Field(None, alias='libraryBranchId')

    model_config = {'populate_by_name': True}


class LibraryBranchByUserQueryParams(LibraryBranchParentQueryParams):
    client_id: UUID4 | None = Field(None, alias='clientId')

    model_config = {'populate_by_name': True}
