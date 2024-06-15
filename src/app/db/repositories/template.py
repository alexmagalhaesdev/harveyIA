from sqlalchemy.orm import Session
from db.models.template import Template
from schemas.template import TemplateSchema


def create_new_template(user_id, template: TemplateSchema, db: Session):
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


def get_all_templates(user_id: str, db: Session):
    templates_in_db = db.query(Template).filter(Template.user_id == user_id).all()
    return templates_in_db


def update_template():
    pass


def delete_template():
    pass
