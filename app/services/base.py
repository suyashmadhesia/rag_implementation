from typing import Optional, Dict, Any, List
from fastapi import  Request, Response, UploadFile
from pydantic import BaseModel

class BaseService:
    def __init__(
        self,
        request: Optional[Request] = None,
        query: Optional[BaseModel] = None,
        response: Optional[Response] = None,
        body: Optional[BaseModel] = None,
        headers: Optional[Dict[str, Any]] = {},
        files: Optional[List[UploadFile]] = None,
        **kwargs: Any
    ):
        self.request = request
        self.query = query
        self.response = response
        self.body = body
        self.headers = headers
        self.files = files
        self.kwargs = kwargs

    
    def handle(self):
        raise NotImplementedError

