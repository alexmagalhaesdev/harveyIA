import os
from pydantic_settings import BaseSettings
from core.load_env import load_env

load_env()


class DatabaseSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_DB: str
    DATABASE_URL: str

    @classmethod
    def from_env_file(cls):
        return cls(
            POSTGRES_USER=os.getenv("POSTGRES_USER"),
            POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD"),
            POSTGRES_HOST=os.getenv("POSTGRES_HOST"),
            POSTGRES_DB=os.getenv("POSTGRES_DB"),
            DATABASE_URL=f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}/{os.getenv('POSTGRES_DB')}?sslmode=require",
        )
