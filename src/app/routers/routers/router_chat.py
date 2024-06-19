from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import HTMLResponse
from core.security.auth_bearer import JWTBearer
from core.ui_config import templates

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
)
def get_chat(request: Request):
    return templates.TemplateResponse("pages/dashboard.html", {"request": request})
