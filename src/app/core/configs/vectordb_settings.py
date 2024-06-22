import os
from pydantic_settings import BaseSettings
from core.load_env import load_env

load_env()


class VectorDBSettings(BaseSettings):
    QDRANT_ENDPOINT: str
    QDRANT_API_KEY: str
    QDRANT_COLLECTION: str

    @classmethod
    def from_env_file(cls):
        return cls(
            QDRANT_COLLECTION=os.getenv("QDRANT_COLLECTION"),
            QDRANT_ENDPOINT=os.getenv("QDRANT_ENDPOINT"),
            QDRANT_API_KEY=os.getenv("QDRANT_API_KEY"),
        )
