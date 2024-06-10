from db.base_class import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    phone_number = Column(Integer, nullable=False, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    documents = relationship("Document", back_populates="user")
    chat_messages = relationship("ChatMessage", back_populates="user")
    templates = relationship("Template", back_populates="user")
    integrations = relationship("Integration", back_populates="user")
