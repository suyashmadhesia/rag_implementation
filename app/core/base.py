from torch import Tensor
from app.configs.connection import WeaviateClient
from .embeddings import SentenceTransformerEmbeddings
from fastapi import UploadFile

class BasePipeline:

    """Base class for all pipelines."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._weaviate_client = WeaviateClient()

    def _process_file(self, filename: str, contents: bytes) -> str:
        raise NotImplementedError
    
    async def _store_embeddings(self, embeddings : Tensor):
        client = await self._weaviate_client.client()
        
    async def process(self, file_id, file : UploadFile) -> None:
        content = await file.read()
        file_text: str = self._process_file(file.filename, content)
        transformer = SentenceTransformerEmbeddings(file_text, self.model_name)
        embeddings = transformer.generate_embeddings()
        await self._store_embeddings(embeddings)
        

    