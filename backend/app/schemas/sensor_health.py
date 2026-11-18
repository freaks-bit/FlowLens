
from datetime import datetime
from typing import Literal

from pydantic import BaseModel


SensorHealthStatus = Literal[
    "recent",
    "stale",
    "offline",
    "maintenance",
    "inactive",
    "never_seen",
]


class SensorHealthRead(BaseModel):
    sensor_id: int
    sensor_name: str
    serial_number: str
    zone_id: int
    zone_name: str
    reported_status: str
    health_status: SensorHealthStatus
    is_active: bool
    last_seen_at: datetime | None
    minutes_since_last_seen: float | None


class SiteSensorHealthRead(BaseModel):
    site_id: int
    site_name: str
    checked_at: datetime
    stale_after_minutes: int

    total_sensors: int
    recent_count: int
    stale_count: int
    offline_count: int
    maintenance_count: int
    inactive_count: int
    never_seen_count: int

    sensors: list[SensorHealthRead]
