from .base import BaseService
from app.schemas.response_schemas import UploadFileResponse
from app.core.pipelines import *
from fastapi import HTTPException


class FileUploadService(BaseService):

    async def _process_file(self, filename: str, session_id: str):
        if filename.endswith(".pdf"):
            return await PDFIngestionPipeline(session_id=session_id).process(self.files[0])
        elif filename.endswith(".docx"):
            return await DocxIngestionPipeline(session_id=session_id).process(self.files[0])
        elif filename.endswith(".txt"):
            return await TextIngestionPipeline(session_id=session_id).process(self.files[0])
        elif filename.endswith(".json"):
            return await JSONIngestionPipeline(session_id=session_id).process(self.files[0])
        else:
            raise ValueError("Unsupported file type")

    async def handle(self):
        session_id = self.headers.get("request_id")
        if not session_id:
            raise HTTPException(status_code=400, detail="Session ID is required")
        if not self.files or len(self.files) != 1:
            raise HTTPException(
                status_code=400, detail="Only one file can be uploaded at a time"
            )
        file =self.files[0]
        try:
            canonical_id = await self._process_file(file.filename, session_id)
            return UploadFileResponse(
                filename=file.filename,
                file_id=canonical_id,
                status=201,
                message="File uploaded successfully",
            )
        except ValueError:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
