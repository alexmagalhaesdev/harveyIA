import os
from pydantic_settings import BaseSettings
from core.load_env import load_env

load_env()


class JWTTokenSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str

    @classmethod
    def from_env_file(cls):
        return cls(
            SECRET_KEY=os.getenv("SECRET_KEY"),
            ALGORITHM=os.getenv("ALGORITHM"),
        )
