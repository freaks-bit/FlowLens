
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.sensor_health import SiteSensorHealthRead
from app.services.sensor_health_service import (
    SensorHealthService,
)


router = APIRouter(tags=["sensor-health"])


@router.get(
    "/sites/{site_id}/sensor-health",
    response_model=SiteSensorHealthRead,
)
def get_site_sensor_health(
    site_id: int,
    stale_after_minutes: int = Query(
        default=60,
        ge=1,
        le=10080,
    ),
    db: Session = Depends(get_db),
):
    return SensorHealthService.get_site_sensor_health(
        db=db,
        site_id=site_id,
        stale_after_minutes=stale_after_minutes,
    )
