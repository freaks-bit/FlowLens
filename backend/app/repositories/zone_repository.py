from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.zone import Zone
from app.schemas.zone import ZoneCreate, ZoneUpdate

class ZoneRepository:
    @staticmethod
    def create(db: Session, site_id: int, zone_in: ZoneCreate) -> Zone:
        zone = Zone(site_id=site_id, **zone_in.model_dump())
        db.add(zone)
        db.commit()
        db.refresh(zone)
        return zone

    @staticmethod
    def list_by_site(db: Session, site_id: int, skip: int = 0, limit: int = 100) -> list[Zone]:
        stmt = select(Zone).where(Zone.site_id == site_id).order_by(Zone.id).offset(skip).limit(limit)
        return list(db.scalars(stmt).all())

    @staticmethod
    def get(db: Session, zone_id: int) -> Zone | None:
        return db.get(Zone, zone_id)

    @staticmethod
    def update(db: Session, zone: Zone, zone_in: ZoneUpdate) -> Zone:
        for field, value in zone_in.model_dump(exclude_unset=True).items():
            setattr(zone, field, value)
        db.commit()
        db.refresh(zone)
        return zone

    @staticmethod
    def delete(db: Session, zone: Zone) -> None:
        db.delete(zone)
        db.commit()