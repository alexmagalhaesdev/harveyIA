from db.base_class import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Template(Base):
    id = Column(Integer, primary_key=True, index=True)
    template_name = Column(String, nullable=False, unique=True, index=True)
    template_content = Column(String, nullable=False, unique=True, index=True)
    template_type = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now(), nullable=False)

    user = relationship("User", back_populates="templates")
