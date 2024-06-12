# Application EntryPoint
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from core.config import settings
from routers.base import router
from pathlib import Path
import uvicorn


# Define the base directory of the project
BASE_DIR = Path(__file__).resolve().parent

# Create an instance of Jinja2Templates, specifying the directory for templates
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Create an instance of StaticFiles, specifying the directory for static files
static_files = StaticFiles(directory=str(BASE_DIR / "static"))


def include_router(app):
    """Function to include the router in the FastAPI app."""
    app.include_router(router)


def start_application():
    """Function to create and configure the FastAPI application."""
    # Create a FastAPI app instance with a title and version from settings
    app = FastAPI(title=settings.project_title, version=settings.project_version)

    # Include the router with all defined routes
    include_router(app)

    # Mount the route for serving static files
    app.mount("/static", static_files, name="static")

    return app


# Instantiate the FastAPI application
app = start_application()


# Entry point for running the application directly
if __name__ == "__main__":
    # Run the application using uvicorn with hot-reloading enabled
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
