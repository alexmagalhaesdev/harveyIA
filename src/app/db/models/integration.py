from db.base_class import Base
from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Integration(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    integration_type = Column(
        Enum("WhatsApp", "Gmail", "Outlook"), nullable=False, index=True
    )
    created_at = Column(DateTime, default=func.now(), nullable=False)

    user = relationship("User", back_populates="integrations")
