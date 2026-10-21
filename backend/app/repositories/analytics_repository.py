from datetime import datetime

from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from app.models.count_event import CountEvent
from app.models.sensor import Sensor
from app.models.zone import Zone


class AnalyticsRepository:
    @staticmethod
    def get_zone_occupancy_raw(
        db: Session,
        zone_id: int,
    ):
        occupancy_expression = func.coalesce(
            func.sum(
                case(
                    (CountEvent.direction == "IN", CountEvent.count),
                    (CountEvent.direction == "OUT", -CountEvent.count),
                    else_=0,
                )
            ),
            0,
        )

        statement = (
            select(
                Zone.id.label("zone_id"),
                Zone.name.label("zone_name"),
                Zone.capacity.label("capacity"),
                occupancy_expression.label("occupancy"),
            )
            .outerjoin(Sensor, Sensor.zone_id == Zone.id)
            .outerjoin(CountEvent, CountEvent.sensor_id == Sensor.id)
            .where(Zone.id == zone_id)
            .group_by(
                Zone.id,
                Zone.name,
                Zone.capacity,
            )
        )

        return db.execute(statement).mappings().first()

    @staticmethod
    def list_site_zone_occupancy_raw(
        db: Session,
        site_id: int,
    ):
        occupancy_expression = func.coalesce(
            func.sum(
                case(
                    (CountEvent.direction == "IN", CountEvent.count),
                    (CountEvent.direction == "OUT", -CountEvent.count),
                    else_=0,
                )
            ),
            0,
        )

        statement = (
            select(
                Zone.id.label("zone_id"),
                Zone.name.label("zone_name"),
                Zone.capacity.label("capacity"),
                occupancy_expression.label("occupancy"),
            )
            .outerjoin(Sensor, Sensor.zone_id == Zone.id)
            .outerjoin(CountEvent, CountEvent.sensor_id == Sensor.id)
            .where(Zone.site_id == site_id)
            .group_by(
                Zone.id,
                Zone.name,
                Zone.capacity,
            )
            .order_by(Zone.id)
        )

        return db.execute(statement).mappings().all()

    @staticmethod
    def get_zone_occupancy_history_raw(
        db: Session,
        zone_id: int,
        start_at: datetime,
        end_at: datetime,
    ):
        event_delta = case(
            (CountEvent.direction == "IN", CountEvent.count),
            (CountEvent.direction == "OUT", -CountEvent.count),
            else_=0,
        )

        baseline_statement = (
            select(
                func.coalesce(
                    func.sum(event_delta),
                    0,
                ).label("baseline_occupancy")
            )
            .select_from(CountEvent)
            .join(
                Sensor,
                Sensor.id == CountEvent.sensor_id,
            )
            .where(
                Sensor.zone_id == zone_id,
                CountEvent.occurred_at < start_at,
            )
        )

        baseline_occupancy = db.execute(
            baseline_statement
        ).scalar_one()

        events_statement = (
            select(
                CountEvent.occurred_at.label("timestamp"),
                event_delta.label("delta"),
            )
            .join(
                Sensor,
                Sensor.id == CountEvent.sensor_id,
            )
            .where(
                Sensor.zone_id == zone_id,
                CountEvent.occurred_at >= start_at,
                CountEvent.occurred_at <= end_at,
            )
            .order_by(
                CountEvent.occurred_at,
                CountEvent.id,
            )
        )

        events = db.execute(
            events_statement
        ).mappings().all()

        return baseline_occupancy, events