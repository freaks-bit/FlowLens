from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.analytics import (
    SiteOccupancyRead,
    ZoneOccupancyHistoryRead,
    ZoneOccupancyRead,
)
from app.services.analytics_service import AnalyticsService


router = APIRouter(tags=["analytics"])

@router.get(
    "/zones/{zone_id}/occupancy",
    response_model=ZoneOccupancyRead,
)
def get_zone_occupancy(
    zone_id: int,
    db: Session = Depends(get_db),
):
    return AnalyticsService.get_zone_occupancy(
        db,
        zone_id,
    )


@router.get(
    "/sites/{site_id}/occupancy",
    response_model=SiteOccupancyRead,
)
def get_site_occupancy(
    site_id: int,
    db: Session = Depends(get_db),
):
    return AnalyticsService.get_site_occupancy(
        db,
        site_id,
    )


@router.get(
    "/zones/{zone_id}/history",
    response_model=ZoneOccupancyHistoryRead,
)
def get_zone_occupancy_history(
    zone_id: int,
    start_at: datetime = Query(...),
    end_at: datetime = Query(...),
    db: Session = Depends(get_db),
):
    return AnalyticsService.get_zone_occupancy_history(
        db,
        zone_id,
        start_at,
        end_at,
    )