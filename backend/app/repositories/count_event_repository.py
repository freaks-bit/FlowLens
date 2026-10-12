from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.count_event import CountEvent
from app.schemas.count_event import CountEventCreate


class CountEventRepository:
    @staticmethod
    def create(
        db: Session,
        sensor_id: int,
        event_in: CountEventCreate,
    ) -> CountEvent:
        event = CountEvent(
            sensor_id=sensor_id,
            **event_in.model_dump(),
        )

        db.add(event)
        db.commit()
        db.refresh(event)
        return event

    @staticmethod
    def list_by_sensor(
        db: Session,
        sensor_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> list[CountEvent]:
        statement = (
            select(CountEvent)
            .where(CountEvent.sensor_id == sensor_id)
            .order_by(CountEvent.occurred_at.desc(), CountEvent.id.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(db.scalars(statement).all())

    @staticmethod
    def get(
        db: Session,
        event_id: int,
    ) -> CountEvent | None:
        return db.get(CountEvent, event_id)