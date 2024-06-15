from fastapi import APIRouter, Request, status
from core.ui_config import templates


router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
def list_all_templates(request: Request):
    templates_in_db = []
    return templates.TemplateResponse(
        "pages/templates.html", {"request": request, "templates": templates_in_db}
    )
