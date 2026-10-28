from fastapi import APIRouter

from app.api.v1.alert_rules import (
    router as alert_rules_router,
)
from app.api.v1.analytics import (
    router as analytics_router,
)
from app.api.v1.count_events import (
    router as count_events_router,
)
from app.api.v1.sensors import (
    router as sensors_router,
)
from app.api.v1.sites import (
    router as sites_router,
)
from app.api.v1.zones import (
    router as zones_router,
)

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(sites_router)

api_router.include_router(zones_router)

api_router.include_router(sensors_router)

api_router.include_router(count_events_router)

api_router.include_router(analytics_router)

api_router.include_router(alert_rules_router)
