from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.sensor import SensorCreate, SensorRead, SensorUpdate
from app.services.sensor_service import SensorService

router = APIRouter(tags=["sensors"])


@router.post(
    "/zones/{zone_id}/sensors",
    response_model=SensorRead,
    status_code=status.HTTP_201_CREATED,
)
def create_sensor(zone_id: int, sensor_in: SensorCreate, db: Session = Depends(get_db)):
    return SensorService.create(db, zone_id, sensor_in)


@router.get("/zones/{zone_id}/sensors", response_model=list[SensorRead])
def list_sensors_for_zone(
    zone_id: int,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return SensorService.list_by_zone(db, zone_id, skip, limit)


@router.get("/sensors/{sensor_id}", response_model=SensorRead)
def get_sensor(sensor_id: int, db: Session = Depends(get_db)):
    return SensorService.get(db, sensor_id)


@router.patch("/sensors/{sensor_id}", response_model=SensorRead)
def update_sensor(sensor_id: int, sensor_in: SensorUpdate, db: Session = Depends(get_db)):
    return SensorService.update(db, sensor_id, sensor_in)


@router.delete("/sensors/{sensor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sensor(sensor_id: int, db: Session = Depends(get_db)):
    SensorService.delete(db, sensor_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)