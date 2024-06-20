import os
from pydantic_settings import BaseSettings
from core.load_env import load_env

load_env()


class VectorDBSettings(BaseSettings):
    QDRANT_ENDPOINT: str
    QDRANT_CLIENT: str

    @classmethod
    def from_env_file(cls):
        return cls(
            QDRANT_ENDPOINT=os.getenv("QDRANT_ENDPOINT"),
            QDRANT_CLIENT=os.getenv("QDRANT_CLIENT"),
        )
