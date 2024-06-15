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
def list_all_legal_sources(request: Request):
    legal_sources = []
    return templates.TemplateResponse(
        "pages/legal_source.html", {"request": request, "legal_sources": legal_sources}
    )
