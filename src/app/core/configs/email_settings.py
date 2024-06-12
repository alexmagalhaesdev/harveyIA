import os
from pydantic import EmailStr
from pydantic_settings import BaseSettings
from core.load_env import load_env

load_env()


class EmailSettings(BaseSettings):
    MAILGUN_SENDER: EmailStr
    MAILGUN_DOMAIN: str
    MAILGUN_API_KEY: str

    @classmethod
    def from_env_file(cls):
        return cls(
            MAILGUN_SENDER=os.getenv("MAILGUN_SENDER"),
            MAILGUN_DOMAIN=os.getenv("MAILGUN_DOMAIN"),
            MAILGUN_API_KEY=os.getenv("MAILGUN_API_KEY"),
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
