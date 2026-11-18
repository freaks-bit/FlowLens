r"""Seed a fresh Neon database with synthetic FlowLens facility monitoring data.

Run from C:\Projects\FlowLens\backend in a shell configured for Neon:
    python seed_demo.py

Safety: refuses non-Neon targets and databases that already contain sites.
The dataset is fictional and for demonstration only.
"""

from __future__ import annotations

from datetime import datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import engine

SITE_NAME = "FlowLens Demo Mall (Simulated)"
TIMEZONE = ZoneInfo("Asia/Kuala_Lumpur")


def local_datetime(day, hour: int, minute: int = 0) -> datetime:
    return datetime.combine(day, time(hour, minute), tzinfo=TIMEZONE)


def add_event(connection, sensor_id: int, direction: str, count: int, when: datetime) -> None:
    connection.execute(
        text(
            """
            INSERT INTO count_events
                (sensor_id, direction, count, occurred_at, received_at)
            VALUES
                (:sensor_id, :direction, :count, :occurred_at, :received_at)
            """
        ),
        {
            "sensor_id": sensor_id,
            "direction": direction,
            "count": count,
            "occurred_at": when,
            "received_at": when + timedelta(seconds=3),
        },
    )


def main() -> None:
    # The local PostgreSQL database must never be seeded accidentally.
    host = (engine.url.host or "").lower()
    if not host.endswith(".neon.tech") or engine.url.database != "neondb":
        raise SystemExit(
            "STOP: This script only seeds the Neon 'neondb' database. "
            "Keep using the terminal with your temporary Neon credentials."
        )

    now = datetime.now(timezone.utc)
    today = now.astimezone(TIMEZONE).date()

    try:
        # All writes commit together, or all roll back on an error.
        with engine.begin() as connection:
            database, username = connection.execute(
                text("SELECT current_database(), current_user")
            ).one()
            print(f"Connected to Neon database: {database} (user: {username})")

            existing_sites = connection.execute(
                text("SELECT COUNT(*) FROM sites")
            ).scalar_one()
            if existing_sites:
                print(
                    "No changes made: this database already has a site. "
                    "The seed script is designed for a fresh demo database."
                )
                return

            site_id = connection.execute(
                text(
                    """
                    INSERT INTO sites
                        (name, address, timezone, capacity, created_at, updated_at)
                    VALUES
                        (:name, :address, :timezone, :capacity, :now, :now)
                    RETURNING id
                    """
                ),
                {
                    "name": SITE_NAME,
                    "address": "Fictional facility, Johor Bahru, Malaysia",
                    "timezone": "Asia/Kuala_Lumpur",
                    "capacity": 850,
                    "now": now,
                },
            ).scalar_one()

            if site_id != 1:
                raise RuntimeError(
                    f"Expected the fresh demo site's ID to be 1, got {site_id}. "
                    "Transaction rolled back; verify the site ID used by the frontend."
                )

            zones = [
                ("Main Entrance", "ENTRANCE_MAIN", "Ground Floor", 350),
                ("Food Court", "FOOD_COURT", "Level 1", 500),
            ]
            zone_ids = []
            for name, code, floor, capacity in zones:
                zone_id = connection.execute(
                    text(
                        """
                        INSERT INTO zones
                            (site_id, name, code, floor_label, capacity,
                             is_active, created_at, updated_at)
                        VALUES
                            (:site_id, :name, :code, :floor_label, :capacity,
                             TRUE, :now, :now)
                        RETURNING id
                        """
                    ),
                    {
                        "site_id": site_id,
                        "name": name,
                        "code": code,
                        "floor_label": floor,
                        "capacity": capacity,
                        "now": now,
                    },
                ).scalar_one()
                zone_ids.append(zone_id)

            sensors = [
                (zone_ids[0], "Main Entrance Counter", "FL-ENT-DEMO-001"),
                (zone_ids[1], "Food Court Counter", "FL-FC-DEMO-001"),
            ]
            sensor_ids = []
            for zone_id, name, serial in sensors:
                sensor_id = connection.execute(
                    text(
                        """
                        INSERT INTO sensors
                            (zone_id, name, serial_number, status, installed_at,
                             last_seen_at, is_active, created_at, updated_at)
                        VALUES
                            (:zone_id, :name, :serial, 'online', :installed_at,
                             :last_seen_at, TRUE, :now, :now)
                        RETURNING id
                        """
                    ),
                    {
                        "zone_id": zone_id,
                        "name": name,
                        "serial": serial,
                        "installed_at": now - timedelta(days=35),
                        "last_seen_at": now - timedelta(minutes=4),
                        "now": now,
                    },
                ).scalar_one()
                sensor_ids.append(sensor_id)

            # Balanced days keep cumulative occupancy realistic for FlowLens's
            # IN-minus-OUT calculation. Time series covers the last 28 days.
            event_count = 0
            for days_ago in range(28, 0, -1):
                day = today - timedelta(days=days_ago)
                n = 28 - days_ago

                entrance_morning = 36 + (n % 6) * 4
                entrance_midday = 20 + (n % 4) * 3
                entrance_afternoon_out = 25 + (n % 3) * 3
                entrance_evening = 12 + (n % 4) * 2
                entrance_close = (
                    entrance_morning + entrance_midday
                    - entrance_afternoon_out + entrance_evening
                )
                entrance_events = [
                    ("IN", entrance_morning, 9, 30),
                    ("IN", entrance_midday, 12, 10),
                    ("OUT", entrance_afternoon_out, 15, 30),
                    ("IN", entrance_evening, 18, 0),
                    ("OUT", entrance_close, 21, 30),
                ]

                food_morning = 48 + (n % 7) * 5
                food_lunch = 22 + (n % 4) * 4
                food_afternoon_out = 30 + (n % 5) * 2
                food_evening = 15 + (n % 3) * 5
                food_close = (
                    food_morning + food_lunch
                    - food_afternoon_out + food_evening
                )
                food_events = [
                    ("IN", food_morning, 10, 30),
                    ("IN", food_lunch, 12, 30),
                    ("OUT", food_afternoon_out, 16, 0),
                    ("IN", food_evening, 18, 30),
                    ("OUT", food_close, 22, 0),
                ]

                for sensor_id, events in (
                    (sensor_ids[0], entrance_events),
                    (sensor_ids[1], food_events),
                ):
                    for direction, count, hour, minute in events:
                        add_event(
                            connection,
                            sensor_id,
                            direction,
                            count,
                            local_datetime(day, hour, minute),
                        )
                        event_count += 1

            # Recent simulated events leave a visible current occupancy:
            # Entrance: 48 IN - 6 OUT = 42 people.
            # Food Court: 74 IN - 20 OUT = 54 people.
            recent = [
                (sensor_ids[0], "IN", 48, 18),
                (sensor_ids[1], "IN", 74, 15),
                (sensor_ids[0], "OUT", 6, 9),
                (sensor_ids[1], "OUT", 20, 4),
            ]
            for sensor_id, direction, count, minutes_ago in recent:
                add_event(
                    connection,
                    sensor_id,
                    direction,
                    count,
                    now - timedelta(minutes=minutes_ago),
                )
                event_count += 1

            # One intentionally triggered low threshold demonstrates alerts;
            # higher thresholds demonstrate non-triggered configured rules.
            rules = [
                (zone_ids[0], "Demo Entrance Advisory (10%)", 10.0),
                (zone_ids[0], "Entrance Critical (90%)", 90.0),
                (zone_ids[1], "Food Court Warning (70%)", 70.0),
            ]
            for zone_id, name, threshold in rules:
                connection.execute(
                    text(
                        """
                        INSERT INTO alert_rules
                            (zone_id, name, rule_type, threshold,
                             is_enabled, created_at, updated_at)
                        VALUES
                            (:zone_id, :name, 'utilization_percent', :threshold,
                             TRUE, :now, :now)
                        """
                    ),
                    {"zone_id": zone_id, "name": name,
                     "threshold": threshold, "now": now},
                )

        print("Demo seed committed successfully.")
        print(f"Site ID: {site_id}; zones: {zone_ids}; sensors: {sensor_ids}")
        print(f"Simulated visitor events: {event_count}; alert rules: {len(rules)}")
        print("Expected occupancy: Entrance 42, Food Court 54, Site total 96")
        print("All data is synthetic; do not describe it as real sensor activity.")
    except (SQLAlchemyError, RuntimeError) as exc:
        print(f"Seed failed; the transaction was rolled back. {exc}")
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
