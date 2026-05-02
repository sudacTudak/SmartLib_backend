from pydantic import BaseModel, Field, UUID4

__all__ = ['ListByWorkQueryParams', 'AvailabilityInfoByWorkQueryParams']


class ListByWorkQueryParams(BaseModel):
    work_id: UUID4 | None = Field(None, alias='workId')
    only_available: bool | None = Field(None, alias='onlyAvailable')

    model_config = {
        'populate_by_name': True
    }


class AvailabilityInfoByWorkQueryParams(BaseModel):
    work_id: UUID4 | None = Field(None, alias='workId')

    model_config = {
        'populate_by_name': True
    }
