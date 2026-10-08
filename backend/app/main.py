from fastapi import FastAPI

app = FastAPI(
    title="FlowLens API",
    description="REST API for the FlowLens smart space analytics platform.",
    version="0.1.0",
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