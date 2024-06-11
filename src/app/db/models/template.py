from db.base_class import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func


class Template(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    template_name = Column(String, nullable=False, unique=True, index=True)
    template_content = Column(String, nullable=False, unique=True, index=True)
    template_type = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
