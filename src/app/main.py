from fastapi import FastAPI

from core.config import settings


def start_application():
    app = FastAPI(title=settings.project_title, version=settings.project_version)
    return app


start_application()
