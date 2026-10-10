from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


SensorStatus = Literal["online", "offline", "maintenance"]


class SensorBase(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    serial_number: str = Field(min_length=3, max_length=120)
    status: SensorStatus = "offline"
    installed_at: datetime | None = None
    last_seen_at: datetime | None = None
    is_active: bool = True


class SensorCreate(SensorBase):
    pass


class SensorUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=160)
    status: SensorStatus | None = None
    installed_at: datetime | None = None
    last_seen_at: datetime | None = None
    is_active: bool | None = None


class SensorRead(SensorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    zone_id: int
    created_at: datetime
    updated_at: datetime