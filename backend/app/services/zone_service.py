from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.zone import Zone
from app.repositories.site_repository import SiteRepository
from app.repositories.zone_repository import ZoneRepository
from app.schemas.zone import ZoneCreate, ZoneUpdate

class ZoneService:
    @staticmethod
    def _ensure_site_exists(db: Session, site_id: int) -> None:
        if SiteRepository.get(db, site_id) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found")

    @staticmethod
    def create(db: Session, site_id: int, zone_in: ZoneCreate) -> Zone:
        ZoneService._ensure_site_exists(db, site_id)
        return ZoneRepository.create(db, site_id, zone_in)

    @staticmethod
    def list_by_site(db: Session, site_id: int, skip: int = 0, limit: int = 100) -> list[Zone]:
        ZoneService._ensure_site_exists(db, site_id)
        return ZoneRepository.list_by_site(db, site_id, skip, limit)

    @staticmethod
    def get(db: Session, zone_id: int) -> Zone:
        zone = ZoneRepository.get(db, zone_id)
        if zone is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Zone not found")
        return zone

    @staticmethod
    def update(db: Session, zone_id: int, zone_in: ZoneUpdate) -> Zone:
        return ZoneRepository.update(db, ZoneService.get(db, zone_id), zone_in)

    @staticmethod
    def delete(db: Session, zone_id: int) -> None:
        ZoneRepository.delete(db, ZoneService.get(db, zone_id))