from .base import BaseService
from app.schemas.response_schemas import UploadFileResponse
from app.utils.media_utils import process_pdf, process_docx, process_json
from fastapi import HTTPException


class FileUploadService(BaseService):

    def _process_file(self, filename: str, contents: bytes):
        if filename.endswith(".pdf"):
            return process_pdf(contents)
        elif filename.endswith(".docx"):
            return process_docx(contents)
        elif filename.endswith(".txt"):
            return contents.decode("utf-8")
        elif filename.endswith(".json"):
            return process_json(contents)
        else:
            raise ValueError("Unsupported file type")

    async def handle(self):
        if not self.files or len(self.files) != 1:
            raise HTTPException(
                status_code=400, detail="Only one file can be uploaded at a time"
            )
        file_id, file_obj = next(iter(self.files.items()))

        try:
            content = await file_obj.read()
            file_text: str = self._process_file(file_obj.filename, content)

            return UploadFileResponse(
                filename=file_obj.filename,
                file_id=str(file_id),
                status=201,
                message="File uploaded successfully",
            )
        except ValueError:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
