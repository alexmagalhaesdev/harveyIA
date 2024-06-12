import os
from pydantic import EmailStr
from typing import Optional
from pydantic_settings import BaseSettings
from core.load_env import load_env

load_env()


class EmailSettings(BaseSettings):
    EMAIL_SENDER: Optional[EmailStr] = None
    EMAIL_API_KEY: Optional[str] = None

    @classmethod
    def from_env_file(cls):
        return cls(
            EMAIL_SENDER=os.getenv("EMAIL_SENDER"),
            EMAIL_API_KEY=os.getenv("EMAIL_API_KEY"),
        )


print("Configurações de e-mail carregadas:", EmailSettings.from_env_file())
