from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.alert_rule import AlertRule
from app.repositories.alert_rule_repository import (
    AlertRuleRepository,
)
from app.repositories.zone_repository import (
    ZoneRepository,
)
from app.schemas.alert_rule import (
    AlertRuleCreate,
    AlertRuleUpdate,
)


class AlertRuleService:
    @staticmethod
    def _get_zone_or_404(
        db: Session,
        zone_id: int,
    ):
        zone = ZoneRepository.get(
            db,
            zone_id,
        )

        if zone is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Zone not found",
            )

        return zone

    @staticmethod
    def _get_rule_or_404(
        db: Session,
        rule_id: int,
    ) -> AlertRule:
        rule = AlertRuleRepository.get(
            db,
            rule_id,
        )

        if rule is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alert rule not found",
            )

        return rule

    @staticmethod
    def _validate_threshold(
        rule_type: str,
        threshold: float,
    ) -> None:
        if (
            rule_type == "utilization_percent"
            and threshold > 100
        ):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=(
                    "Utilization percent threshold "
                    "cannot exceed 100"
                ),
            )

    @staticmethod
    def create(
        db: Session,
        zone_id: int,
        rule_in: AlertRuleCreate,
    ) -> AlertRule:
        AlertRuleService._get_zone_or_404(
            db,
            zone_id,
        )

        AlertRuleService._validate_threshold(
            rule_in.rule_type,
            rule_in.threshold,
        )

        return AlertRuleRepository.create(
            db,
            zone_id,
            rule_in,
        )

    @staticmethod
    def list_by_zone(
        db: Session,
        zone_id: int,
    ) -> list[AlertRule]:
        AlertRuleService._get_zone_or_404(
            db,
            zone_id,
        )

        return AlertRuleRepository.list_by_zone(
            db,
            zone_id,
        )

    @staticmethod
    def get(
        db: Session,
        rule_id: int,
    ) -> AlertRule:
        return AlertRuleService._get_rule_or_404(
            db,
            rule_id,
        )

    @staticmethod
    def update(
        db: Session,
        rule_id: int,
        rule_in: AlertRuleUpdate,
    ) -> AlertRule:
        rule = AlertRuleService._get_rule_or_404(
            db,
            rule_id,
        )

        rule_type = (
            rule_in.rule_type
            if rule_in.rule_type is not None
            else rule.rule_type
        )

        threshold = (
            rule_in.threshold
            if rule_in.threshold is not None
            else rule.threshold
        )

        AlertRuleService._validate_threshold(
            rule_type,
            threshold,
        )

        return AlertRuleRepository.update(
            db,
            rule,
            rule_in,
        )

    @staticmethod
    def delete(
        db: Session,
        rule_id: int,
    ) -> None:
        rule = AlertRuleService._get_rule_or_404(
            db,
            rule_id,
        )

        AlertRuleRepository.delete(
            db,
            rule,
        )