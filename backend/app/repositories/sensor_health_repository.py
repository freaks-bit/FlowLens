
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.sensor import Sensor
from app.models.zone import Zone


class SensorHealthRepository:
    @staticmethod
    def list_by_site(
        db: Session,
        site_id: int,
    ):
        statement = (
            select(
                Sensor,
                Zone.name.label("zone_name"),
            )
            .join(
                Zone,
                Sensor.zone_id == Zone.id,
            )
            .where(Zone.site_id == site_id)
            .order_by(
                Zone.id.asc(),
                Sensor.id.asc(),
            )
        )

        return db.execute(statement).all()
