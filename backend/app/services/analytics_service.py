from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.alert_rule_repository import (
    AlertRuleRepository,
)
from app.repositories.analytics_repository import (
    AnalyticsRepository,
)
from app.repositories.site_repository import (
    SiteRepository,
)
from app.repositories.zone_repository import (
    ZoneRepository,
)
from app.schemas.analytics import (
    OccupancyHistoryPoint,
    SiteOccupancyRead,
    TriggeredAlertRead,
    ZoneOccupancyHistoryRead,
    ZoneOccupancyRead,
)


class AnalyticsService:
    @staticmethod
    def _status_for(
        utilization_percent: float,
    ) -> str:
        if utilization_percent >= 90:
            return "critical"

        if utilization_percent >= 70:
            return "warning"

        return "normal"

    @staticmethod
    def _evaluate_alert_rules(
        db: Session,
        zone_id: int,
        occupancy: int,
        utilization_percent: float,
    ) -> list[TriggeredAlertRead]:
        rules = (
            AlertRuleRepository.list_by_zone(
                db,
                zone_id,
            )
        )

        triggered_alerts: list[
            TriggeredAlertRead
        ] = []

        for rule in rules:
            if not rule.is_enabled:
                continue

            if (
                rule.rule_type
                == "utilization_percent"
            ):
                current_value = (
                    utilization_percent
                )

            elif rule.rule_type == "occupancy":
                current_value = float(
                    occupancy
                )

            else:
                continue

            if current_value < rule.threshold:
                continue

            triggered_alerts.append(
                TriggeredAlertRead(
                    rule_id=rule.id,
                    name=rule.name,
                    rule_type=rule.rule_type,
                    threshold=rule.threshold,
                    current_value=current_value,
                )
            )

        return triggered_alerts

    @staticmethod
    def _build_zone_payload(
        db: Session,
        row,
    ) -> ZoneOccupancyRead:
        capacity = int(
            row["capacity"] or 0
        )

        occupancy = max(
            int(
                row["occupancy"] or 0
            ),
            0,
        )

        available_capacity = max(
            capacity - occupancy,
            0,
        )

        utilization_percent = (
            round(
                (
                    occupancy
                    / capacity
                )
                * 100,
                2,
            )
            if capacity > 0
            else 0.0
        )

        triggered_alerts = (
            AnalyticsService
            ._evaluate_alert_rules(
                db=db,
                zone_id=row["zone_id"],
                occupancy=occupancy,
                utilization_percent=(
                    utilization_percent
                ),
            )
        )

        return ZoneOccupancyRead(
            zone_id=row["zone_id"],
            zone_name=row["zone_name"],
            capacity=capacity,
            occupancy=occupancy,
            available_capacity=(
                available_capacity
            ),
            utilization_percent=(
                utilization_percent
            ),
            status=(
                AnalyticsService
                ._status_for(
                    utilization_percent
                )
            ),
            triggered_alerts=(
                triggered_alerts
            ),
        )

    @staticmethod
    def get_zone_occupancy(
        db: Session,
        zone_id: int,
    ) -> ZoneOccupancyRead:
        if (
            ZoneRepository.get(
                db,
                zone_id,
            )
            is None
        ):
            raise HTTPException(
                status_code=(
                    status.HTTP_404_NOT_FOUND
                ),
                detail="Zone not found",
            )

        row = (
            AnalyticsRepository
            .get_zone_occupancy_raw(
                db,
                zone_id,
            )
        )

        return (
            AnalyticsService
            ._build_zone_payload(
                db,
                row,
            )
        )

    @staticmethod
    def get_site_occupancy(
        db: Session,
        site_id: int,
    ) -> SiteOccupancyRead:
        site = SiteRepository.get(
            db,
            site_id,
        )

        if site is None:
            raise HTTPException(
                status_code=(
                    status.HTTP_404_NOT_FOUND
                ),
                detail="Site not found",
            )

        rows = (
            AnalyticsRepository
            .list_site_zone_occupancy_raw(
                db,
                site_id,
            )
        )

        zones = [
            AnalyticsService
            ._build_zone_payload(
                db,
                row,
            )
            for row in rows
        ]

        total_capacity = sum(
            zone.capacity
            for zone in zones
        )

        total_occupancy = sum(
            zone.occupancy
            for zone in zones
        )

        available_capacity = max(
            total_capacity
            - total_occupancy,
            0,
        )

        utilization_percent = (
            round(
                (
                    total_occupancy
                    / total_capacity
                )
                * 100,
                2,
            )
            if total_capacity > 0
            else 0.0
        )

        return SiteOccupancyRead(
            site_id=site.id,
            site_name=site.name,
            total_capacity=(
                total_capacity
            ),
            total_occupancy=(
                total_occupancy
            ),
            available_capacity=(
                available_capacity
            ),
            utilization_percent=(
                utilization_percent
            ),
            zones=zones,
        )

    @staticmethod
    def get_zone_occupancy_history(
        db: Session,
        zone_id: int,
        start_at: datetime,
        end_at: datetime,
    ) -> ZoneOccupancyHistoryRead:
        zone = ZoneRepository.get(
            db,
            zone_id,
        )

        if zone is None:
            raise HTTPException(
                status_code=(
                    status.HTTP_404_NOT_FOUND
                ),
                detail="Zone not found",
            )

        if start_at >= end_at:
            raise HTTPException(
                status_code=(
                    status.HTTP_400_BAD_REQUEST
                ),
                detail=(
                    "start_at must be "
                    "before end_at"
                ),
            )

        baseline_occupancy, events = (
            AnalyticsRepository
            .get_zone_occupancy_history_raw(
                db,
                zone_id,
                start_at,
                end_at,
            )
        )

        current_occupancy = max(
            int(
                baseline_occupancy or 0
            ),
            0,
        )

        points = [
            OccupancyHistoryPoint(
                timestamp=start_at,
                occupancy=(
                    current_occupancy
                ),
            )
        ]

        for event in events:
            current_occupancy = max(
                current_occupancy
                + int(event["delta"]),
                0,
            )

            points.append(
                OccupancyHistoryPoint(
                    timestamp=(
                        event[
                            "timestamp"
                        ]
                    ),
                    occupancy=(
                        current_occupancy
                    ),
                )
            )

        return ZoneOccupancyHistoryRead(
            zone_id=zone.id,
            zone_name=zone.name,
            start_at=start_at,
            end_at=end_at,
            points=points,
        )