from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


EventDirection = Literal["IN", "OUT"]


class CountEventCreate(BaseModel):
    direction: EventDirection
    count: int = Field(default=1, ge=1)
    occurred_at: datetime


class CountEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sensor_id: int
    direction: EventDirection
    count: int
    occurred_at: datetime
    received_at: datetime