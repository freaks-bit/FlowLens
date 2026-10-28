from fastapi import (
    APIRouter,
    Depends,
    status,
)
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.alert_rule import (
    AlertRuleCreate,
    AlertRuleRead,
    AlertRuleUpdate,
)
from app.services.alert_rule_service import (
    AlertRuleService,
)


router = APIRouter(
    tags=["alert-rules"]
)


@router.post(
    "/zones/{zone_id}/alert-rules",
    response_model=AlertRuleRead,
    status_code=status.HTTP_201_CREATED,
)
def create_alert_rule(
    zone_id: int,
    rule_in: AlertRuleCreate,
    db: Session = Depends(get_db),
):
    return AlertRuleService.create(
        db,
        zone_id,
        rule_in,
    )


@router.get(
    "/zones/{zone_id}/alert-rules",
    response_model=list[AlertRuleRead],
)
def list_alert_rules_for_zone(
    zone_id: int,
    db: Session = Depends(get_db),
):
    return AlertRuleService.list_by_zone(
        db,
        zone_id,
    )


@router.get(
    "/alert-rules/{rule_id}",
    response_model=AlertRuleRead,
)
def get_alert_rule(
    rule_id: int,
    db: Session = Depends(get_db),
):
    return AlertRuleService.get(
        db,
        rule_id,
    )


@router.patch(
    "/alert-rules/{rule_id}",
    response_model=AlertRuleRead,
)
def update_alert_rule(
    rule_id: int,
    rule_in: AlertRuleUpdate,
    db: Session = Depends(get_db),
):
    return AlertRuleService.update(
        db,
        rule_id,
        rule_in,
    )


@router.delete(
    "/alert-rules/{rule_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_alert_rule(
    rule_id: int,
    db: Session = Depends(get_db),
):
    AlertRuleService.delete(
        db,
        rule_id,
    )