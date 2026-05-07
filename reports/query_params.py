from datetime import date

from pydantic import BaseModel, Field, UUID4

__all__ = ['ReportQueryParams']


class ReportQueryParams(BaseModel):
    library_branch_id: UUID4 | None = Field(None, alias='libraryBranchId')
    date_from: date | None = Field(None, alias='dateFrom')
    date_to: date | None = Field(None, alias='dateTo')
    include_closed_loans: bool | None = Field(False, alias='includeClosedLoans')

    model_config = {
        'populate_by_name': True,
    }
