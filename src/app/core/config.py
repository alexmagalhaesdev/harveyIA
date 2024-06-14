import os
from pydantic_settings import BaseSettings
from core.load_env import load_env

from core.configs.database_settings import DatabaseSettings
from core.configs.email_settings import EmailSettings
from core.configs.storage_settings import StorageSettings
from core.configs.payment_settings import PaymentSettings

load_env()


class Settings(BaseSettings):
    project_title: str
    project_version: str
    database: DatabaseSettings
    email: EmailSettings
    storage: StorageSettings
    payment: PaymentSettings

    @classmethod
    def from_env_file(cls):
        return cls(
            project_title=os.getenv("PROJECT_TITLE", "HarveyAI"),
            project_version=os.getenv("PROJECT_VERSION", "0.1.0"),
            database=DatabaseSettings.from_env_file(),
            email=EmailSettings.from_env_file(),
            storage=StorageSettings.from_env_file(),
            payment=PaymentSettings.from_env_file(),
        )


settings = Settings.from_env_file()
