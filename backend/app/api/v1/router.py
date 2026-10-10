from fastapi import APIRouter
from app.api.v1.sites import router as sites_router
from app.api.v1.zones import router as zones_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(sites_router)
api_router.include_router(zones_router)