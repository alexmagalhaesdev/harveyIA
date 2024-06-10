from fastapi import FastAPI

from core.config import settings


def start_application():
    app = FastAPI(title=settings.PROJECT_TITLE, version=settings.PROJECT_VERSION)
    return app


start_application()
