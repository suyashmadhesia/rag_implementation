import uuid
from pydantic import BaseModel

class HealthCheckResponse(BaseModel):
    status: int
    message: str

class UploadFileResponse(BaseModel):
    filename: str
    file_id: str
    status: int
    message: str