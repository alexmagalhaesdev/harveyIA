import os
from pydantic_settings import BaseSettings
from core.load_env import load_env

load_env()


class PaymentSettings(BaseSettings):
    PAYMENT_PUBLISHABLE_KEY: str
    PAYMENT_SECRET_KEY: str

    @classmethod
    def from_env_file(cls):
        return cls(
            PAYMENT_PUBLISHABLE_KEY=os.getenv("PAYMENT_PUBLISHABLE_KEY"),
            EMAIL_API_KEY=os.getenv("PAYMENT_SECRET_KEY"),
        )
