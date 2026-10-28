from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.count_event import CountEvent
from app.repositories.count_event_repository import (
    CountEventRepository,
)
from app.repositories.sensor_repository import (
    SensorRepository,
)
from app.schemas.count_event import (
    CountEventCreate,
    RecentCountEventRead,
)


class CountEventService:
    @staticmethod
    def _get_sensor_or_404(
        db: Session,
        sensor_id: int,
    ):
        sensor = SensorRepository.get(
            db,
            sensor_id,
        )

        if sensor is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sensor not found",
            )

        return sensor

    @staticmethod
    def create(
        db: Session,
        sensor_id: int,
        event_in: CountEventCreate,
    ) -> CountEvent:
        sensor = (
            CountEventService._get_sensor_or_404(
                db,
                sensor_id,
            )
        )

        if not sensor.is_active:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Sensor is inactive",
            )

        event = CountEventRepository.create(
            db,
            sensor_id,
            event_in,
        )

        sensor.last_seen_at = datetime.now(
            timezone.utc
        )
        sensor.status = "online"

        db.commit()

        return event

    @staticmethod
    def list_by_sensor(
        db: Session,
        sensor_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> list[CountEvent]:
        CountEventService._get_sensor_or_404(
            db,
            sensor_id,
        )

        return (
            CountEventRepository.list_by_sensor(
                db,
                sensor_id,
                skip,
                limit,
            )
        )

    @staticmethod
    def get(
        db: Session,
        event_id: int,
    ) -> CountEvent:
        event = CountEventRepository.get(
            db,
            event_id,
        )

        if event is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Count event not found",
            )

        return event

    @staticmethod
    def list_recent(
        db: Session,
        limit: int = 10,
    ) -> list[RecentCountEventRead]:
        rows = CountEventRepository.list_recent(
            db,
            limit,
        )

        return [
            RecentCountEventRead(
                event_id=row["event_id"],
                sensor_id=row["sensor_id"],
                sensor_name=row["sensor_name"],
                zone_id=row["zone_id"],
                zone_name=row["zone_name"],
                direction=row["direction"],
                count=row["count"],
                occurred_at=row["occurred_at"],
            )
            for row in rows
        ]