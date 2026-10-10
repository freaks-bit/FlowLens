from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class ZoneBase(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    code: str = Field(min_length=2, max_length=60)
    floor_label: str | None = Field(default=None, max_length=60)
    capacity: int = Field(default=0, ge=0)
    is_active: bool = True

class ZoneCreate(ZoneBase):
    pass

class ZoneUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=160)
    code: str | None = Field(default=None, min_length=2, max_length=60)
    floor_label: str | None = Field(default=None, max_length=60)
    capacity: int | None = Field(default=None, ge=0)
    is_active: bool | None = None

class ZoneRead(ZoneBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    site_id: int
    created_at: datetime
    updated_at: datetime