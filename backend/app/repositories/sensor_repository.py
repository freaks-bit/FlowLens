from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.sensor import Sensor
from app.schemas.sensor import SensorCreate, SensorUpdate


class SensorRepository:
    @staticmethod
    def create(db: Session, zone_id: int, sensor_in: SensorCreate) -> Sensor:
        sensor = Sensor(zone_id=zone_id, **sensor_in.model_dump())
        db.add(sensor)
        db.commit()
        db.refresh(sensor)
        return sensor

    @staticmethod
    def list_by_zone(db: Session, zone_id: int, skip: int = 0, limit: int = 100) -> list[Sensor]:
        statement = (
            select(Sensor)
            .where(Sensor.zone_id == zone_id)
            .order_by(Sensor.id)
            .offset(skip)
            .limit(limit)
        )
        return list(db.scalars(statement).all())

    @staticmethod
    def get(db: Session, sensor_id: int) -> Sensor | None:
        return db.get(Sensor, sensor_id)

    @staticmethod
    def get_by_serial(db: Session, serial_number: str) -> Sensor | None:
        statement = select(Sensor).where(Sensor.serial_number == serial_number)
        return db.scalar(statement)

    @staticmethod
    def update(db: Session, sensor: Sensor, sensor_in: SensorUpdate) -> Sensor:
        for field, value in sensor_in.model_dump(exclude_unset=True).items():
            setattr(sensor, field, value)
        db.commit()
        db.refresh(sensor)
        return sensor

    @staticmethod
    def delete(db: Session, sensor: Sensor) -> None:
        db.delete(sensor)
        db.commit()