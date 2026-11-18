
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.sensor_health_repository import (
    SensorHealthRepository,
)
from app.repositories.site_repository import SiteRepository
from app.schemas.sensor_health import (
    SensorHealthRead,
    SensorHealthStatus,
    SiteSensorHealthRead,
)


class SensorHealthService:
    @staticmethod
    def _evaluate_status(
        reported_status: str,
        is_active: bool,
        last_seen_at: datetime | None,
        now: datetime,
        stale_after_minutes: int,
    ) -> tuple[SensorHealthStatus, float | None]:
        minutes_since_last_seen = None

        if last_seen_at is not None:
            if last_seen_at.tzinfo is None:
                last_seen_at = last_seen_at.replace(
                    tzinfo=timezone.utc,
                )

            minutes_since_last_seen = round(
                max(
                    0,
                    (now - last_seen_at).total_seconds()
                    / 60,
                ),
                1,
            )

        if not is_active:
            health_status = "inactive"

        elif reported_status == "maintenance":
            health_status = "maintenance"

        elif reported_status == "offline":
            health_status = "offline"

        elif last_seen_at is None:
            health_status = "never_seen"

        elif minutes_since_last_seen > stale_after_minutes:
            health_status = "stale"

        else:
            health_status = "recent"

        return health_status, minutes_since_last_seen

    @staticmethod
    def get_site_sensor_health(
        db: Session,
        site_id: int,
        stale_after_minutes: int = 60,
    ) -> SiteSensorHealthRead:
        site = SiteRepository.get(db, site_id)

        if site is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Site not found",
            )

        now = datetime.now(timezone.utc)

        rows = SensorHealthRepository.list_by_site(
            db,
            site_id,
        )

        sensors: list[SensorHealthRead] = []

        counts = {
            "recent": 0,
            "stale": 0,
            "offline": 0,
            "maintenance": 0,
            "inactive": 0,
            "never_seen": 0,
        }

        for sensor, zone_name in rows:
            health_status, age_minutes = (
                SensorHealthService._evaluate_status(
                    reported_status=sensor.status,
                    is_active=sensor.is_active,
                    last_seen_at=sensor.last_seen_at,
                    now=now,
                    stale_after_minutes=stale_after_minutes,
                )
            )

            counts[health_status] += 1

            sensors.append(
                SensorHealthRead(
                    sensor_id=sensor.id,
                    sensor_name=sensor.name,
                    serial_number=sensor.serial_number,
                    zone_id=sensor.zone_id,
                    zone_name=zone_name,
                    reported_status=sensor.status,
                    health_status=health_status,
                    is_active=sensor.is_active,
                    last_seen_at=sensor.last_seen_at,
                    minutes_since_last_seen=age_minutes,
                )
            )

        return SiteSensorHealthRead(
            site_id=site.id,
            site_name=site.name,
            checked_at=now,
            stale_after_minutes=stale_after_minutes,
            total_sensors=len(sensors),
            recent_count=counts["recent"],
            stale_count=counts["stale"],
            offline_count=counts["offline"],
            maintenance_count=counts["maintenance"],
            inactive_count=counts["inactive"],
            never_seen_count=counts["never_seen"],
            sensors=sensors,
        )
