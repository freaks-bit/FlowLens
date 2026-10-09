from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SiteBase(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    address: str | None = Field(default=None, max_length=500)
    timezone: str = Field(default="Asia/Kuala_Lumpur", max_length=80)
    capacity: int = Field(default=0, ge=0)


class SiteCreate(SiteBase):
    pass


class SiteUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=160)
    address: str | None = Field(default=None, max_length=500)
    timezone: str | None = Field(default=None, max_length=80)
    capacity: int | None = Field(default=None, ge=0)


class SiteRead(SiteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime