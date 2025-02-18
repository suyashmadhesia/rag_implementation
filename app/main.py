from typing import List
import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, File, UploadFile
from app.configs.connection import WeaviateClient
from app.services.health_check_service import HealthCheckService
from app.services.file_upload_service import FileUploadService
from app.schemas.response_schemas import HealthCheckResponse, UploadFileResponse

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

@app.get("/api/health-check", response_model=HealthCheckResponse)
async def health_check():
    return HealthCheckService().handle()


@app.post("/api/upload", response_model=List[UploadFileResponse])
async def upload_files(files: List[UploadFile] = File(...)):
    """API to upload multiple files at once."""
    file_dict = {uuid.uuid4(): file for file in files}
    return await FileUploadService(files=file_dict).handle()