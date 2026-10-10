from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.sensor import Sensor
from app.repositories.sensor_repository import SensorRepository
from app.repositories.zone_repository import ZoneRepository
from app.schemas.sensor import SensorCreate, SensorUpdate


class SensorService:
    @staticmethod
    def _ensure_zone_exists(db: Session, zone_id: int) -> None:
        if ZoneRepository.get(db, zone_id) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Zone not found",
            )

    @staticmethod
    def _ensure_serial_is_available(db: Session, serial_number: str) -> None:
        if SensorRepository.get_by_serial(db, serial_number) is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Sensor serial number already exists",
            )

    @staticmethod
    def create(db: Session, zone_id: int, sensor_in: SensorCreate) -> Sensor:
        SensorService._ensure_zone_exists(db, zone_id)
        SensorService._ensure_serial_is_available(db, sensor_in.serial_number)
        return SensorRepository.create(db, zone_id, sensor_in)

    @staticmethod
    def list_by_zone(db: Session, zone_id: int, skip: int = 0, limit: int = 100) -> list[Sensor]:
        SensorService._ensure_zone_exists(db, zone_id)
        return SensorRepository.list_by_zone(db, zone_id, skip, limit)

    @staticmethod
    def get(db: Session, sensor_id: int) -> Sensor:
        sensor = SensorRepository.get(db, sensor_id)
        if sensor is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sensor not found",
            )
        return sensor

    @staticmethod
    def update(db: Session, sensor_id: int, sensor_in: SensorUpdate) -> Sensor:
        return SensorRepository.update(db, SensorService.get(db, sensor_id), sensor_in)

    @staticmethod
    def delete(db: Session, sensor_id: int) -> None:
        SensorRepository.delete(db, SensorService.get(db, sensor_id))