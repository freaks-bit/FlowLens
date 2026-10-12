from pydantic import BaseModel, ConfigDict


class ZoneOccupancyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    zone_id: int
    zone_name: str
    capacity: int
    occupancy: int
    available_capacity: int
    utilization_percent: float
    status: str


class SiteOccupancyRead(BaseModel):
    site_id: int
    site_name: str
    total_capacity: int
    total_occupancy: int
    available_capacity: int
    utilization_percent: float
    zones: list[ZoneOccupancyRead]