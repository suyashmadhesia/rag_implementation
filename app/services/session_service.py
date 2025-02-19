from fastapi import HTTPException, Response
from .base import BaseService
from app.utils.storage import LocalStorage


class SessionService(BaseService):

    def __init__(self, query = None, response = None, body = None, headers = None, files = None, request=None,**kwargs):
        super().__init__(request, query, response, body, headers, files, **kwargs)
        self.local_storage = LocalStorage()

    def _create_session(self):
        session_id = self.local_storage.create_session()
        self.response.set_cookie(key="request_id", value=session_id, httponly=True)
        return {
            "message": "ok"
        }
    

    def _fetch_session_details(self):
        session_id = self.headers.get("request_id")
        if not session_id:
            raise HTTPException(status_code=400, detail="Session ID is required")
        session_details = self.local_storage.get_session(session_id)
        session_files = self.local_storage.get_session_file(session_id)
        if not session_details:
            raise HTTPException(status_code=404, detail="Session not found")
        return {
            "message": "ok",
            "session": session_details.to_json(),
            "files": session_files
        }
    
    def _delete_session(self):
        session_id = self.headers.get("request_id")
        if not session_id:
            raise HTTPException(status_code=400, detail="Session ID is required")
        session_details = self.local_storage.get_session(session_id)
        if not session_details:
            raise HTTPException(status_code=404, detail="Session not found")
        self.local_storage.delete_session(session_id)
        self.response.delete_cookie("request_id")
        self.response.delete_cookie("session_id")
        return {
            "message": "ok"
        }

    def handle(self, path):
        if path == "create":
            return self._create_session()
        elif path == "fetch":
            return self._fetch_session_details()
        elif path == "delete":
            return self._delete_session()
        else:
            raise NotImplementedError("Unsupported path")
    