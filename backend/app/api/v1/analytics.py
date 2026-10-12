from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.analytics import SiteOccupancyRead, ZoneOccupancyRead
from app.services.analytics_service import AnalyticsService

router = APIRouter(tags=["analytics"])


@router.get(
    "/analytics/zones/{zone_id}/occupancy",
    response_model=ZoneOccupancyRead,
)
def get_zone_occupancy(
    zone_id: int,
    db: Session = Depends(get_db),
):
    return AnalyticsService.get_zone_occupancy(db, zone_id)


@router.get(
    "/analytics/sites/{site_id}/occupancy",
    response_model=SiteOccupancyRead,
)
def get_site_occupancy(
    site_id: int,
    db: Session = Depends(get_db),
):
    return AnalyticsService.get_site_occupancy(db, site_id)