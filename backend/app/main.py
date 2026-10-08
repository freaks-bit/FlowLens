from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="FlowLens API",
    description="REST API for the FlowLens smart space analytics platform.",
    version="0.1.0",
)

allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "name": "FlowLens API",
        "version": "0.1.0",
        "status": "running",
    }

@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "service": "flowlens-api",
    }