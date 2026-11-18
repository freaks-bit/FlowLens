
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.api.v1.router import api_router
from app.core.config import settings
from app.db.session import engine


app = FastAPI(
    title="FlowLens API",
    description=(
        "REST API for the FlowLens facility "
        "occupancy and sensor monitoring platform."
    ),
    version="0.1.0",
)


# Protect the public demo against changes to stored data.
@app.middleware("http")
async def enforce_read_only_demo(request: Request, call_next):
    allowed_methods = {"GET", "HEAD", "OPTIONS"}

    if (
        settings.demo_read_only
        and request.method.upper() not in allowed_methods
    ):
        return JSONResponse(
            status_code=403,
            content={
                "detail": (
                    "This FlowLens demo is read-only. "
                    "Data modification is disabled."
                )
            },
        )

    return await call_next(request)


# CORS origins are configured through environment variables.
allowed_origins = [
    origin.strip().rstrip("/")
    for origin in settings.cors_origins.split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router)


@app.get("/")
def root():
    return {
        "name": "FlowLens API",
        "version": "0.1.0",
        "status": "running",
        "demo_read_only": settings.demo_read_only,
    }


@app.get("/api/v1/health")
def health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "service": "flowlens-api",
            "database": "connected",
        }

    except SQLAlchemyError:
        return {
            "status": "degraded",
            "service": "flowlens-api",
            "database": "unavailable",
        }
