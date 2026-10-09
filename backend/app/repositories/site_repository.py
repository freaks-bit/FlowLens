from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.site import Site
from app.schemas.site import SiteCreate, SiteUpdate


class SiteRepository:
    @staticmethod
    def create(db: Session, site_in: SiteCreate) -> Site:
        site = Site(**site_in.model_dump())
        db.add(site)
        db.commit()
        db.refresh(site)
        return site

    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 100) -> list[Site]:
        statement = (
            select(Site)
            .order_by(Site.id)
            .offset(skip)
            .limit(limit)
        )
        return list(db.scalars(statement).all())

    @staticmethod
    def get(db: Session, site_id: int) -> Site | None:
        return db.get(Site, site_id)

    @staticmethod
    def update(
        db: Session,
        site: Site,
        site_in: SiteUpdate,
    ) -> Site:
        for field, value in site_in.model_dump(exclude_unset=True).items():
            setattr(site, field, value)

        db.commit()
        db.refresh(site)
        return site

    @staticmethod
    def delete(db: Session, site: Site) -> None:
        db.delete(site)
        db.commit()