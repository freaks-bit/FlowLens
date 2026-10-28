from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.alert_rule import AlertRule
from app.schemas.alert_rule import (
    AlertRuleCreate,
    AlertRuleUpdate,
)


class AlertRuleRepository:
    @staticmethod
    def create(
        db: Session,
        zone_id: int,
        rule_in: AlertRuleCreate,
    ) -> AlertRule:
        rule = AlertRule(
            zone_id=zone_id,
            **rule_in.model_dump(),
        )

        db.add(rule)
        db.commit()
        db.refresh(rule)

        return rule

    @staticmethod
    def list_by_zone(
        db: Session,
        zone_id: int,
    ) -> list[AlertRule]:
        statement = (
            select(AlertRule)
            .where(
                AlertRule.zone_id == zone_id
            )
            .order_by(
                AlertRule.threshold.asc(),
                AlertRule.id.asc(),
            )
        )

        return list(
            db.scalars(statement).all()
        )

    @staticmethod
    def get(
        db: Session,
        rule_id: int,
    ) -> AlertRule | None:
        return db.get(
            AlertRule,
            rule_id,
        )

    @staticmethod
    def update(
        db: Session,
        rule: AlertRule,
        rule_in: AlertRuleUpdate,
    ) -> AlertRule:
        update_data = rule_in.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(
                rule,
                field,
                value,
            )

        db.commit()
        db.refresh(rule)

        return rule

    @staticmethod
    def delete(
        db: Session,
        rule: AlertRule,
    ) -> None:
        db.delete(rule)
        db.commit()