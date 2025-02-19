from fastapi import Response
from .base import BaseService
from app.utils.storage import LocalStorage


class SessionService(BaseService):

    def __init__(self, query = None, response = None, body = None, headers = None, files = None, **kwargs):
        super().__init__(query, response, body, headers, files, **kwargs)
        self.local_storage = LocalStorage()

    def _create_session(self):
        session_id = self.local_storage.create_session()
        self.response.set_cookie(key="session_id", value=session_id, httponly=True)
        return {
            "message": "ok"
        }
    

    def _fetch_session_details(self):
        session_id = self.headers.get("session_id")
        if not session_id:
            return {
                "message": "session_id not found"
            }
        session_details = self.local_storage.get_session(session_id)
        session_files = self.local_storage.get_session_file(session_id)
        if not session_details:
            return {
                "message": "session not found"
            }
        return {
            "message": "ok",
            "session": session_details.to_json(),
            "files": session_files
        }

    def handle(self, path):
        if path == "create":
            return self._create_session()
        elif path == "fetch":
            return 
        else:
            raise NotImplementedError("Unsupported path")
    