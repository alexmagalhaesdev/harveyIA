from sqlalchemy.orm import Session
from db.models.template import Template
from schemas.template import TemplateSchema


def create_new_template(template: TemplateSchema, user_id: int, db: Session):
    new_template = Template(
        user_id=user_id,
        template_name=template.template_name,
        template_content=template.template_content,
        template_type=template.template_type,
    )

    db.add(new_template)
    db.commit()

    db.refresh(new_template)
    return new_template


def get_all_templates(user_id: int, db: Session):
    templates_in_db = db.query(Template).filter_by(user_id=user_id).all()
    return templates_in_db


def get_template_by_id(template_id: int, user_id: int, db: Session):
    template_in_db = (
        db.query(Template)
        .filter(Template.user_id == user_id)
        .filter(Template.id == template_id)
    )
    return template_in_db


def update_template_by_id(
    template_id: int, user_id: int, updated_template: TemplateSchema, db: Session
):
    template_in_db = (
        db.query(Template)
        .filter(Template.user_id == user_id)
        .filter(Template.id == template_id)
    )

    for field, value in updated_template.dict(exclude_unset=True).items():
        setattr(template_in_db, field, value)

    db.commit()
    db.refresh(template_in_db)

    return template_in_db


def delete_template_by_id(template_id: int, user_id: int, db: Session):
    template_in_db = (
        db.query(Template)
        .filter(Template.user_id == user_id)
        .filter(Template.id == template_id)
    )

    if not template_in_db.first():
        return {
            "error": f"Could not find template with id {template_id} for user with id {user_id}"
        }

    template_in_db.delete()
    db.commit()

    return {
        "message": f"Deleted template with id {template_id} for user with id {user_id}"
    }
