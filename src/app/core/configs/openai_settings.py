import os
from pydantic_settings import BaseSettings
from core.load_env import load_env

load_env()


class OpenAISettings(BaseSettings):
    OPENAI_API_KEY: str

    @classmethod
    def from_env_file(cls):
        return cls(OPENAI_API_KEY=os.getenv("OPENAI_API_KEY"))
