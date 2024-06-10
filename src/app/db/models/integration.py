from db.base_class import Base
from sqlalchemy import Column, String, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Integration(Base):
    id = Column(Integer, primary_key=True, index=True)
    integration_name = Column(String, nullable=False, unique=True, index=True)
    integration_type = Column(Enum("WhatsApp", "Gmail"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now(), nullable=False)

    user = relationship("User", back_populates="integrations")
