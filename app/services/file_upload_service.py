from .base import BaseService
from app.schemas.response_schemas import UploadFileResponse
from app.utils.media_utils import process_pdf, process_docx, process_json
from fastapi import HTTPException


class FileUploadService(BaseService):

    def _process_file(self, filename: str, contents: bytes):
        if filename.endswith('.pdf'):
            return process_pdf(contents)
        elif filename.endswith('.docx'):
            return process_docx(contents)
        elif filename.endswith('.txt'):
            return contents.decode("utf-8")
        elif filename.endswith('.json'):
            return process_json(contents)
        else:
            raise ValueError("Unsupported file type")

    async def handle(self):
        proccessed_content = []
        for key, value in self.files.items():
            try:
                content = await value.read()
                file_text : str = self._process_file(value.filename, content)
                proccessed_content.append(UploadFileResponse(
                    filename=value.filename,
                    file_id=str(key),
                    status=201,
                    message="File uploaded successfully"
                ))
            except Exception as ValueError:
                raise HTTPException(status_code=400, detail="Unsupported file type")
            except Exception as e:
                proccessed_content.append(UploadFileResponse(
                    filename=value.filename,
                    file_id=str(key),
                    status=500,
                    message=str(e)
                ))
        return proccessed_content
