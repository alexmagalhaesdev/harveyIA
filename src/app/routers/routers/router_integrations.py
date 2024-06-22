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
def list_all_integrations(request: Request):
    integrations = []
    return templates.TemplateResponse(
        "pages/integrations.html", {"request": request, "integrations": integrations}
    )


@router.post(
    "/",
    dependencies=[Depends(JWTBearer())],
    response_class=HTMLResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_integration(request: Request):
    pass


@router.put(
    "/{integration_id}",
    dependencies=[Depends(JWTBearer())],
    response_class=HTMLResponse,
    status_code=status.HTTP_201_CREATED,
)
def update_integration(request: Request):
    pass


@router.delete(
    "/{integration_id}",
    dependencies=[Depends(JWTBearer())],
    response_class=HTMLResponse,
    status_code=status.HTTP_201_CREATED,
)
def delete_integration(request: Request):
    pass
