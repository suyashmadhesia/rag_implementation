import uuid
from torch import Tensor
from app.configs.connection import WeaviateClient
from .embeddings import SentenceTransformerEmbeddings
from fastapi import UploadFile
from app.utils.storage import LocalStorage

class BasePipeline:

    """Base class for all pipelines."""

    def __init__(self, session_id:str, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._session_id = session_id
        self._weaviate_client = WeaviateClient()
        self._local_storage = LocalStorage()

    def _is_storage_available(self):
        return self._local_storage.allow_storing(self._session_id)

    def _process_file(self, contents: bytes) -> str:
        if not self._is_storage_available():
            raise ValueError("Storage limit exceeded")
        raise NotImplementedError
    
    async def _store_embeddings(self, embeddings : Tensor):
        client = await self._weaviate_client.client()
        
    async def process(self, file : UploadFile) -> None:
        file_id = str(uuid.uuid4())
        canonical_id = self._local_storage.store_file(
            session_id=self._session_id,
            file_id=file_id,
            file_name=file.filename,
            file_size=file.size,
            file_type=file.content_type
        )
        content = await file.read()
        file_text: str = self._process_file(content)
        transformer = SentenceTransformerEmbeddings(file_text, self.model_name)
        embeddings = transformer.generate_embeddings()
        await self._store_embeddings(embeddings)
        return canonical_id
        

    