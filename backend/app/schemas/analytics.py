from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TriggeredAlertRead(BaseModel):
    rule_id: int
    name: str
    rule_type: str
    threshold: float
    current_value: float


class ZoneOccupancyRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    zone_id: int
    zone_name: str
    capacity: int
    occupancy: int
    available_capacity: int
    utilization_percent: float
    status: str

    triggered_alerts: list[
        TriggeredAlertRead
    ] = Field(default_factory=list)


class SiteOccupancyRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    site_id: int
    site_name: str
    total_capacity: int
    total_occupancy: int
    available_capacity: int
    utilization_percent: float
    zones: list[ZoneOccupancyRead]


class OccupancyHistoryPoint(BaseModel):
    timestamp: datetime
    occupancy: int


class ZoneOccupancyHistoryRead(BaseModel):
    zone_id: int
    zone_name: str
    start_at: datetime
    end_at: datetime
    points: list[OccupancyHistoryPoint]