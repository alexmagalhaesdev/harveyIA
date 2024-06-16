from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import Annotated
from core.security.auth_bearer import JWTBearer
from core.security.auth import Auth
from db.repositories.user import get_user
from db.repositories.template import (
    get_all_templates,
    get_template_by_id,
    create_new_template,
    update_template_by_id,
    delete_template_by_id,
)
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


@router.put(
    "/{template_id}",
    dependencies=[Depends(JWTBearer())],
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
def update_template(
    template_id: int,
    updated_template: TemplateSchema,
    request: Request,
    current_user: UserCreated = Depends(Auth.get_current_user),
    db: Session = Depends(get_db_session),
):
    user = get_user(current_user, db)
    template_in_db = get_template_by_id(template_id, user.id, db)

    if not template_in_db:
        return {
            "error": f"Template with id {template_id} not found for user with id {user.id}"
        }

    updated_template_data = updated_template.dict(exclude_unset=True)
    updated_template = update_template_by_id(db, template_in_db, updated_template_data)

    return templates.TemplateResponse(
        "pages/template_updated.html",
        {"request": request, "template": updated_template},
    )


@router.delete(
    "/{template_id}",
    dependencies=[Depends(JWTBearer())],
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
)
def delete_template(
    template_id: int,
    request: Request,
    current_user: UserCreated = Depends(Auth.get_current_user),
    db: Session = Depends(get_db_session),
):
    user = get_user(current_user, db)
    template_in_db = get_template_by_id(template_id, user.id, db)

    if not template_in_db:
        return {
            "error": f"Template with id {template_id} not found for user with id {user.id}"
        }

    delete_template_by_id(db, template_in_db)

    return templates.TemplateResponse(
        "pages/template_deleted.html", {"request": request, "template": template_in_db}
    )
