from pydantic import BaseModel, Field

from work_reservations.enums import WorkReservationStatus


class WorkReservationListQueryParams(BaseModel):
    client_id: str | None = Field(None, alias='clientId')
    status: WorkReservationStatus | None = None

    model_config = {
        'populate_by_name': True
    }
