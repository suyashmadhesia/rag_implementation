import os
import asyncio
import logging
from weaviate import WeaviateAsyncClient
from weaviate.connect import ConnectionParams
from weaviate.classes.query import Filter
from weaviate.exceptions import WeaviateConnectionError

logger = logging.getLogger(__name__)

class WeaviateClient:
    """Async Singleton class for managing Weaviate connections."""

    _instance = None
    _lock = asyncio.Lock()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._client = None
            cls._instance._host = os.getenv("WEAVIATE_HOST", "localhost")
            cls._instance._http_port = int(os.getenv("WEAVIATE_HTTP_PORT", 8080))
            cls._instance._grpc_port = int(os.getenv("WEAVIATE_GRPC_PORT", 50051))
            cls._instance._http_secure = os.getenv("WEAVIATE_HTTP_SECURE", "false").lower() == "true"
            cls._instance._grpc_secure = os.getenv("WEAVIATE_GRPC_SECURE", "false").lower() == "true"
        return cls._instance

    async def init(self):
        """Initialize Weaviate async client."""
        async with self._lock:
            if self._client is None:
                try:
                    connection_params = ConnectionParams.from_params(
                        http_host=self._host,
                        http_port=self._http_port,
                        http_secure=self._http_secure,
                        grpc_host=self._host,
                        grpc_port=self._grpc_port,
                        grpc_secure=self._grpc_secure
                    )
                    self._client = WeaviateAsyncClient(connection_params=connection_params)
                    await self._client.connect()
                    if not self._client.is_connected():
                        raise WeaviateConnectionError("Weaviate is not ready.")
                    print(f"Connected to Weaviate at {self._host}:{self._http_port}")
                except Exception as e:
                    raise WeaviateConnectionError(f"Failed to connect to Weaviate: {e}")

    async def client(self) -> WeaviateAsyncClient:
        """Return the Weaviate async client instance."""
        print(self.client)
        if self._client is None:
            await self.init()
        return self._client
    
    async def clear_database(self):
        """Delete all objects from all classes in Weaviate."""
        """Delete all objects from all collections in Weaviate v4 async client."""
        if self._client is None:
            await self.init()
        
        try:
            # Get list of all collections
            collection = self._client.collections.get("DocumentChunk")
            collection.data.delete_many(
                where=Filter.by_property("name").like("DocumentChunk*"),
            )

            print("✅ Weaviate database cleared.")
        except Exception as e:
            print(f"❌ Error clearing Weaviate database: {e}")
    
    async def close(self):
        """Properly close the Weaviate async client connection."""
        if self._client is not None:
            try:
                await self.clear_database()  # Empty the database before closing
                await self._client.close()
                print("Weaviate client connection closed.")
            except Exception as e:
                print(f"Error closing Weaviate client: {e}")
            finally:
                self._client = None
