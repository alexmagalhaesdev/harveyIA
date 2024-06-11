from fastapi import FastAPI
from core.config import settings
from routers.base import router


def include_router(app):
    app.include_router(router)


def start_application():
    app = FastAPI(title=settings.project_title, version=settings.project_title)
    include_router(app)
    return app


app = start_application()
