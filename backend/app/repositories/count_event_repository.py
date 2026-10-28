from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.count_event import CountEvent
from app.models.sensor import Sensor
from app.models.zone import Zone
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
            .where(
                CountEvent.sensor_id == sensor_id
            )
            .order_by(
                CountEvent.occurred_at.desc(),
                CountEvent.id.desc(),
            )
            .offset(skip)
            .limit(limit)
        )

        return list(
            db.scalars(statement).all()
        )

    @staticmethod
    def get(
        db: Session,
        event_id: int,
    ) -> CountEvent | None:
        return db.get(
            CountEvent,
            event_id,
        )

    @staticmethod
    def list_recent(
        db: Session,
        limit: int = 10,
    ):
        statement = (
            select(
                CountEvent.id.label("event_id"),
                CountEvent.sensor_id.label(
                    "sensor_id"
                ),
                Sensor.name.label(
                    "sensor_name"
                ),
                Zone.id.label("zone_id"),
                Zone.name.label("zone_name"),
                CountEvent.direction.label(
                    "direction"
                ),
                CountEvent.count.label("count"),
                CountEvent.occurred_at.label(
                    "occurred_at"
                ),
            )
            .join(
                Sensor,
                Sensor.id
                == CountEvent.sensor_id,
            )
            .join(
                Zone,
                Zone.id == Sensor.zone_id,
            )
            .order_by(
                CountEvent.occurred_at.desc(),
                CountEvent.id.desc(),
            )
            .limit(limit)
        )

        return (
            db.execute(statement)
            .mappings()
            .all()
        )