import os
from pydantic_settings import BaseSettings
from core.load_env import load_env

load_env()


class StorageSettings(BaseSettings):
    STORAGE_KEY_ID: str
    STORAGE_SECRET_KEY: str
    STORAGE_TOKEN_VALUE: str
    STORAGE_BUCKET_NAME: str
    STORAGE_DEFAULT_FILE_PATH: str
    STORAGE_CONNECTION_URL: str

    @classmethod
    def from_env_file(cls):
        return cls(
            STORAGE_KEY_ID=os.getenv("STORAGE_KEY_ID"),
            STORAGE_SECRET_KEY=os.getenv("STORAGE_SECRET_KEY"),
            STORAGE_TOKEN_VALUE=os.getenv("STORAGE_TOKEN_VALUE"),
            STORAGE_BUCKET_NAME=os.getenv("STORAGE_BUCKET_NAME"),
            STORAGE_DEFAULT_FILE_PATH=os.getenv("STORAGE_DEFAULT_FILE_PATH"),
            STORAGE_CONNECTION_URL=f"https://{os.getenv('STORAGE_ACCOUNT_ID')}.r2.cloudflarestorage.com",
        )
