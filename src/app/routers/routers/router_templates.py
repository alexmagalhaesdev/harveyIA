from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import Annotated
from core.security.auth_bearer import JWTBearer
from core.security.auth import Auth
from db.repositories.user import get_user
from db.repositories.template import get_all_templates, create_new_template
from db.session import get_db_session
from core.ui_config import templates
from schemas.user import UserCreated
from schemas.template import TemplateSchema

router = APIRouter()


@router.get(
    "/",
    dependencies=[Depends(JWTBearer())],
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
def list_all_templates(
    request: Request,
    current_user: Annotated[UserCreated, Depends(Auth.get_current_user)],
    db: Annotated[Session, Depends(get_db_session)],
):
    user = get_user(current_user, db)
    templates_in_db = get_all_templates(user.id, db)
    print(f"MEUS TEMPLATES {templates_in_db}")
    return templates.TemplateResponse(
        "pages/templates.html", {"request": request, "templates": templates_in_db}
    )


@router.post(
    "/",
    dependencies=[Depends(JWTBearer())],
    response_class=HTMLResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_template(
    request: Request,
    template: TemplateSchema,
    current_user: UserCreated = Depends(Auth.get_current_user),
    db: Session = Depends(get_db_session),
):
    user = get_user(current_user, db)
    new_template = create_new_template(user.id, template, db)
    return {"my_new_template": new_template}
