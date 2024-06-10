from db.base_class import Base
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Document(Base):
    id = Column(Integer, primary_key=True, index=True)
    document_name = Column(String, nullable=False, unique=True, index=True)
    document_type = Column(Enum("PDF", "DOCX"), nullable=False)
    file_path = Column(String, nullable=False, unique=True, index=True)
    upload_date = Column(DateTime, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now(), nullable=False)

    user = relationship("User", back_populates="documents")
