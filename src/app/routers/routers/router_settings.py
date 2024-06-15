from fastapi import APIRouter, Request, status
from core.ui_config import templates

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
def get_user_settings(request: Request):
    user_settings = []
    return templates.TemplateResponse(
        "pages/settings.html", {"request": request, "user_settings": user_settings}
    )
