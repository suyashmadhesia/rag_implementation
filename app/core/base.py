import uuid
from torch import Tensor
from app.configs.connection import WeaviateClient
from .embeddings import SentenceTransformerEmbeddings
from fastapi import HTTPException, UploadFile
from app.utils.storage import LocalStorage
import weaviate.classes as wvc
from weaviate.collections import CollectionAsync
from weaviate.classes.config import Property, DataType


class BasePipeline:
    """Base class for all pipelines."""

    def __init__(self, session_id: str, model_name: str = "all-MiniLM-L6-v2"):
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

    
    async def _store_embeddings(self, file_id: str, chunks: list[str], embeddings: Tensor):
        """Stores embedded document chunks in Weaviate using v4 async client."""
        client = await self._weaviate_client.client()
        embeddings_list = embeddings.cpu().numpy().tolist()
        if not await client.collections.exists("DocumentChunk"):
            await client.collections.create(
                name="DocumentChunk",
                properties=[
                    Property(name="session_id", data_type=DataType.TEXT),
                    Property(name="file_id", data_type=DataType.TEXT),
                    Property(name="chunk_index", data_type=DataType.INT),
                    Property(name="text", data_type=DataType.TEXT),
                ],
                vectorizer_config=wvc.config.Configure.Vectorizer.none(),
                vector_index_config=wvc.config.Configure.VectorIndex.hnsw(
                    distance_metric=wvc.config.VectorDistances.COSINE
                )
            )
        document_chunks : CollectionAsync = client.collections.get("DocumentChunk")
        for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings_list)):
            await document_chunks.data.insert(
                properties={
                    "session_id": self._session_id,
                    "file_id": file_id,
                    "chunk_index": idx,
                    "text": chunk
                },
                vector=embedding
            )


    async def process(self, file: UploadFile) -> None:
        file_id = str(uuid.uuid4())
        canonical_id = self._local_storage.store_file(
            session_id=self._session_id,
            file_id=file_id,
            file_name=file.filename,
            file_size=file.size,
            file_type=file.content_type,
        )
        content = await file.read()
        file_text: str = self._process_file(content)
        try:
            transformer = SentenceTransformerEmbeddings(file_text, self.model_name)
            embeddings = transformer.generate_embeddings()
            await self._store_embeddings(canonical_id, transformer.chunks, embeddings)
            return canonical_id
        except Exception as e:
            self._local_storage.delete_file(self._session_id, canonical_id)
            raise HTTPException(status_code=500, detail=f"Failed to process file: {e}")
        
