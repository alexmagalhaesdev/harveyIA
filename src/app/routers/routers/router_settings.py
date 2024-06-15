from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import HTMLResponse
from core.security.auth_bearer import JWTBearer
from core.ui_config import templates

router = APIRouter()


@router.get(
    "/",
    dependencies=[Depends(JWTBearer())],
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
def get_user_settings(request: Request):
    user_settings = []
    return templates.TemplateResponse(
        "pages/settings.html", {"request": request, "user_settings": user_settings}
    )
