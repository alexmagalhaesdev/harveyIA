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


@router.post(
    "/",
    dependencies=[Depends(JWTBearer())],
    response_class=HTMLResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_legal_source(request: Request):
    pass


@router.put(
    "/{legal_source_id}",
    dependencies=[Depends(JWTBearer())],
    response_class=HTMLResponse,
    status_code=status.HTTP_201_CREATED,
)
def update_legal_source(request: Request):
    pass


@router.delete(
    "/{legal_source_id}",
    dependencies=[Depends(JWTBearer())],
    response_class=HTMLResponse,
    status_code=status.HTTP_201_CREATED,
)
def delete_legal_source(request: Request):
    pass
