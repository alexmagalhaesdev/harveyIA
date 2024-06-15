from fastapi import APIRouter, Request, status
from core.ui_config import templates

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
def list_all_integrations(request: Request):
    integrations = []
    return templates.TemplateResponse(
        "pages/integrations.html", {"request": request, "integrations": integrations}
    )
