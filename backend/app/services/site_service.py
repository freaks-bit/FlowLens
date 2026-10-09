from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.site import Site
from app.repositories.site_repository import SiteRepository
from app.schemas.site import SiteCreate, SiteUpdate


class SiteService:
    @staticmethod
    def create(db: Session, site_in: SiteCreate) -> Site:
        return SiteRepository.create(db, site_in)

    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 100) -> list[Site]:
        return SiteRepository.list(db, skip=skip, limit=limit)

    @staticmethod
    def get(db: Session, site_id: int) -> Site:
        site = SiteRepository.get(db, site_id)

        if site is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Site not found",
            )

        return site

    @staticmethod
    def update(db: Session, site_id: int, site_in: SiteUpdate) -> Site:
        site = SiteService.get(db, site_id)
        return SiteRepository.update(db, site, site_in)

    @staticmethod
    def delete(db: Session, site_id: int) -> None:
        site = SiteService.get(db, site_id)
        SiteRepository.delete(db, site)