from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.site import SiteCreate, SiteRead, SiteUpdate
from app.services.site_service import SiteService

router = APIRouter(prefix="/sites", tags=["sites"])


@router.post(
    "",
    response_model=SiteRead,
    status_code=status.HTTP_201_CREATED,
)
def create_site(
    site_in: SiteCreate,
    db: Session = Depends(get_db),
):
    return SiteService.create(db, site_in)


@router.get("", response_model=list[SiteRead])
def list_sites(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return SiteService.list(db, skip=skip, limit=limit)


@router.get("/{site_id}", response_model=SiteRead)
def get_site(
    site_id: int,
    db: Session = Depends(get_db),
):
    return SiteService.get(db, site_id)


@router.patch("/{site_id}", response_model=SiteRead)
def update_site(
    site_id: int,
    site_in: SiteUpdate,
    db: Session = Depends(get_db),
):
    return SiteService.update(db, site_id, site_in)


@router.delete(
    "/{site_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_site(
    site_id: int,
    db: Session = Depends(get_db),
):
    SiteService.delete(db, site_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)