from qdrant_client import QdrantClient
from app.core.config import settings

qdrant_client = QdrantClient(
    url=settings.vector_db.QDRANT_ENDPOINT,
    api_key=settings.vector_db.QDRANT_CLIENT,
    prefer_grpc=False,
)
