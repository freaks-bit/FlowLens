from fastapi import (
    APIRouter,
    Depends,
    Query,
    status,
)
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.count_event import (
    CountEventCreate,
    CountEventRead,
    RecentCountEventRead,
)
from app.services.count_event_service import (
    CountEventService,
)


router = APIRouter(
    tags=["count-events"]
)


@router.post(
    "/sensors/{sensor_id}/events",
    response_model=CountEventRead,
    status_code=status.HTTP_201_CREATED,
)
def create_count_event(
    sensor_id: int,
    event_in: CountEventCreate,
    db: Session = Depends(get_db),
):
    return CountEventService.create(
        db,
        sensor_id,
        event_in,
    )


@router.get(
    "/sensors/{sensor_id}/events",
    response_model=list[CountEventRead],
)
def list_count_events_for_sensor(
    sensor_id: int,
    skip: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=100,
        ge=1,
        le=100,
    ),
    db: Session = Depends(get_db),
):
    return CountEventService.list_by_sensor(
        db,
        sensor_id,
        skip,
        limit,
    )


@router.get(
    "/events/recent",
    response_model=list[RecentCountEventRead],
)
def list_recent_count_events(
    limit: int = Query(
        default=10,
        ge=1,
        le=50,
    ),
    db: Session = Depends(get_db),
):
    return CountEventService.list_recent(
        db,
        limit,
    )


@router.get(
    "/events/{event_id}",
    response_model=CountEventRead,
)
def get_count_event(
    event_id: int,
    db: Session = Depends(get_db),
):
    return CountEventService.get(
        db,
        event_id,
    )