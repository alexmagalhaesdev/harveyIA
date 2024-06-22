import os
from pydantic_settings import BaseSettings
from core.load_env import load_env

load_env()


class LLMSettings(BaseSettings):
    GEMINI_API_KEY: str

    @classmethod
    def from_env_file(cls):
        return cls(GEMINI_API_KEY=os.getenv("GEMINI_API_KEY"))
