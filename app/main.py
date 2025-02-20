import asyncio
import uuid
from contextlib import asynccontextmanager
from fastapi import Cookie, FastAPI, File, Request, Response, UploadFile, Query, Request
from app.configs.connection import WeaviateClient
from app.core.embeddings import SentenceTransformerEmbeddings
from app.services.health_check_service import HealthCheckService
from app.services.file_upload_service import FileUploadService
from app.services.session_service import SessionService
from app.schemas.response_schemas import HealthCheckResponse, UploadFileResponse
from app.utils.storage import LocalStorage
from weaviate.classes.query import Filter, MetadataQuery


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ensure Weaviate is initialized on FastAPI startup and properly closed on shutdown."""
    LocalStorage()
    weaviate_client = WeaviateClient()
    await weaviate_client.init()
    
    try:
        yield
    finally:
        # Explicitly close Weaviate client
        await weaviate_client.close()
        
        # Ensure all asyncio tasks are completed before shutdown
        await asyncio.sleep(0)  # Let event loop process pending tasks



app = FastAPI(lifespan=lifespan)


@app.get("/api/health-check", response_model=HealthCheckResponse)
async def health_check():
    return HealthCheckService().handle()


@app.post("/api/session")
async def create_session(response: Response):
    """API to create a new session."""
    return SessionService(response=response).handle("create")


@app.get("/api/session")
async def get_session(request: Request):
    """API to get a session."""
    return SessionService(
        headers={"request_id": request.cookies.get("request_id")}
    ).handle("fetch")


@app.delete("/api/session")
async def delete_session(response: Response, request: Request):
    """API to delete a session."""
    return SessionService(
        headers={"request_id": request.cookies.get("request_id")}, response=response
    ).handle("delete")


@app.post("/api/upload", response_model=UploadFileResponse)
async def upload_file(request: Request, file: UploadFile = File(...)):
    """API to upload a single file."""
    return await FileUploadService(
        files=[file], headers={"request_id": request.cookies.get("request_id")}
    ).handle()

@app.get("/api/query")
async def query_document(request: Request, file_id: str = Query(...), query: str = Query(...)):
    """Retrieve the most relevant text snippet(s) from a queried document stored in Weaviate."""
    
    weaviate_client = WeaviateClient()
    client = await weaviate_client.client()
    
    # Generate query embedding
    embedder = SentenceTransformerEmbeddings(query)
    query_embedding = embedder.generate_embeddings().cpu().numpy()

    # Ensure it's a flat list
    if query_embedding.ndim > 1:
        query_embedding = query_embedding.squeeze().tolist()

    
    # Fetch matching text snippets from Weaviate
    document_chunks = client.collections.get("DocumentChunk")
    
    search_results = await document_chunks.query.near_vector(
    near_vector=query_embedding,
    limit=10,
    filters=Filter.by_property("file_id").equal(file_id),
    return_metadata=MetadataQuery(distance=True)
)


    print(search_results)
    # Extract text snippets
    matched_snippets = [
        {
            "chunk_index": result.properties["chunk_index"],
            "text": result.properties["text"],
            "score": result.metadata.distance
        }
        for result in search_results.objects
    ]
    
    return {"file_id": file_id, "query": query, "matches": matched_snippets}
