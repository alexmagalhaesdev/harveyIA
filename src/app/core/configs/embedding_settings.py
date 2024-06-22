import os
from pydantic_settings import BaseSettings
from core.load_env import load_env

load_env()


class EmbeddingSettings(BaseSettings):
    EMBEDDING_MODEL: str
    EMBEDDING_API_KEY: str

    @classmethod
    def from_env_file(cls):
        return cls(
            EMBEDDING_MODEL=os.getenv("EMBEDDING_MODEL"),
            EMBEDDING_API_KEY=os.getenv("EMBEDDING_API_KEY"),
        )
