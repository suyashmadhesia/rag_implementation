from typing import Annotated, Optional, Union, Dict, Any
from fastapi import FastAPI, Query, Header, Path, Body, UploadFile, File
from pydantic import BaseModel, Field

class BaseService:
    def __init__(
        self,
        query: Optional[BaseModel] = None,
        body: Optional[BaseModel] = None,
        headers: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, UploadFile]] = None,
        **kwargs: Any
    ):
        self.query = query
        self.body = body
        self.headers = headers
        self.files = files
        self.path_params = kwargs

    
    def handle(self):
        raise NotImplementedError

