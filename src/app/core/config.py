import os
from pydantic_settings import BaseSettings
from core.load_env import load_env

from core.configs.database_settings import DatabaseSettings

load_env()


class Settings(BaseSettings):
    project_title: str
    project_version: str
    database: DatabaseSettings = DatabaseSettings.from_env_file()

    @classmethod
    def from_env_file(cls):
        return cls(
            project_title=os.getenv("PROJECT_TITLE", "harveyAI"),
            project_version=os.getenv("PROJECT_VERSION", "0.1.0"),
            database=DatabaseSettings.from_env_file(),
        )


settings = Settings.from_env_file()
