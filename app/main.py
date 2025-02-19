import uuid
from contextlib import asynccontextmanager
from fastapi import Cookie, FastAPI, File, Response, UploadFile
from app.configs.connection import WeaviateClient
from app.services.health_check_service import HealthCheckService
from app.services.file_upload_service import FileUploadService
from app.services.session_service import SessionService
from app.schemas.response_schemas import HealthCheckResponse, UploadFileResponse
from app.utils.storage import LocalStorage

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ensure Weaviate is initialized on FastAPI startup and properly closed on shutdown."""
    LocalStorage()
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


@app.post("/api/session/create")
async def create_session(response: Response):
    """API to create a new session."""
    return SessionService(response=response).handle("create")


@app.get("/api/session/fetch")
async def get_session(session_id: str = Cookie(None)):
    """API to get a session."""
    return SessionService(headers={
        "session_id": session_id
    }).handle("fetch")
    


@app.post("/api/upload", response_model=UploadFileResponse)
async def upload_file(file: UploadFile = File(...)):
    """API to upload a single file."""
    file_dict = {uuid.uuid4(): file}
    return await FileUploadService(files=file_dict).handle()