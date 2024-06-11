from db.base_class import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    phone_number = Column(Integer, nullable=False, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    documents = relationship("Document", backref=backref("user_document"))
    chat_messages = relationship("ChatMessage", backref=backref("user_chat_message"))
    templates = relationship("Template", backref=backref("user_template"))
    integrations = relationship("Integration", backref=backref("user_integration"))
