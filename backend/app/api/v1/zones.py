from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.zone import ZoneCreate, ZoneRead, ZoneUpdate
from app.services.zone_service import ZoneService

router = APIRouter(tags=["zones"])

@router.post("/sites/{site_id}/zones", response_model=ZoneRead, status_code=status.HTTP_201_CREATED)
def create_zone(site_id: int, zone_in: ZoneCreate, db: Session = Depends(get_db)):
    return ZoneService.create(db, site_id, zone_in)

@router.get("/sites/{site_id}/zones", response_model=list[ZoneRead])
def list_zones_for_site(site_id: int, skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=100), db: Session = Depends(get_db)):
    return ZoneService.list_by_site(db, site_id, skip, limit)

@router.get("/zones/{zone_id}", response_model=ZoneRead)
def get_zone(zone_id: int, db: Session = Depends(get_db)):
    return ZoneService.get(db, zone_id)

@router.patch("/zones/{zone_id}", response_model=ZoneRead)
def update_zone(zone_id: int, zone_in: ZoneUpdate, db: Session = Depends(get_db)):
    return ZoneService.update(db, zone_id, zone_in)

@router.delete("/zones/{zone_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_zone(zone_id: int, db: Session = Depends(get_db)):
    ZoneService.delete(db, zone_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)