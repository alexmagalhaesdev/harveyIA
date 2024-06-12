from fastapi.templating import Jinja2Templates
from pathlib import Path
from fastapi.staticfiles import StaticFiles

# Define the base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Create an instance of Jinja2Templates, specifying the directory for templates
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Create an instance of StaticFiles, specifying the directory for static files
static_files = StaticFiles(directory=str(BASE_DIR / "static"))
