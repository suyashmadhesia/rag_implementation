from typing import Optional, Dict, Any
from fastapi import  Response, UploadFile
from pydantic import BaseModel

class BaseService:
    def __init__(
        self,
        query: Optional[BaseModel] = None,
        response: Optional[Response] = None,
        body: Optional[BaseModel] = None,
        headers: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, UploadFile]] = None,
        **kwargs: Any
    ):
        self.query = query
        self.response = response
        self.body = body
        self.headers = headers
        self.files = files
        self.kwargs = kwargs

    
    def handle(self):
        raise NotImplementedError

