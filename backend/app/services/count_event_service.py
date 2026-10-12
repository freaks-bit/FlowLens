from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.count_event import CountEvent
from app.repositories.count_event_repository import CountEventRepository
from app.repositories.sensor_repository import SensorRepository
from app.schemas.count_event import CountEventCreate


class CountEventService:
    @staticmethod
    def _get_sensor_or_404(db: Session, sensor_id: int):
        sensor = SensorRepository.get(db, sensor_id)

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
        sensor = CountEventService._get_sensor_or_404(db, sensor_id)

        if not sensor.is_active:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Sensor is inactive",
            )

        event = CountEventRepository.create(db, sensor_id, event_in)

        sensor.last_seen_at = datetime.now(timezone.utc)
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
        CountEventService._get_sensor_or_404(db, sensor_id)
        return CountEventRepository.list_by_sensor(
            db,
            sensor_id,
            skip,
            limit,
        )

    @staticmethod
    def get(
        db: Session,
        event_id: int,
    ) -> CountEvent:
        event = CountEventRepository.get(db, event_id)

        if event is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Count event not found",
            )

        return event