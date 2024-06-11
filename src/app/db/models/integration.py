from db.base_class import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.sql import func


class Integration(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    integration_name = Column(String, nullable=False, unique=True, index=True)
    integration_type = Column(
        ENUM("WhatsApp", "Gmail", name="integration_type_enum"),
        nullable=False,
        index=True,
    )
    created_at = Column(DateTime, default=func.now(), nullable=False)
