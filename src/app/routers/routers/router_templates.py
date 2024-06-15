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
def list_all_templates(request: Request):
    templates_in_db = []
    return templates.TemplateResponse(
        "pages/templates.html", {"request": request, "templates": templates_in_db}
    )
