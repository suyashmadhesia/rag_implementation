from .base import BaseService


class FileUploadService(BaseService):

    def handle(self):
        return {
            "message": "Uploaded Successfully"
        }