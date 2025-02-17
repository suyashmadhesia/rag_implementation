from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.configs.connection import WeaviateClient
from app.services.health_check_service import HealthCheckService

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ensure Weaviate is initialized on FastAPI startup and properly closed on shutdown."""
    weaviate_client = WeaviateClient()
    await weaviate_client.init()
    try:
        yield
    finally:
        await weaviate_client.close()

app = FastAPI(lifespan=lifespan)

@app.get("/api/health-check")
async def health_check():
    return HealthCheckService().handle()