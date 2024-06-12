import os
from pydantic import EmailStr
from pydantic_settings import BaseSettings
from core.load_env import load_env

load_env()


class EmailSettings(BaseSettings):
    EMAIL_SENDER: EmailStr
    EMAIL_API_KEY: str

    @classmethod
    def from_env_file(cls):
        return cls(
            EMAIL_SENDER=os.getenv("EMAIL_SENDER"),
            EMAIL_API_KEY=os.getenv("EMAIL_API_KEY"),
        )
