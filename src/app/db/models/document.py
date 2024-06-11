from db.base_class import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.sql import func


class Document(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    document_name = Column(String, nullable=False, unique=True, index=True)
    document_type = Column(
        ENUM("PDF", "DOCX", name="document_type_enum"), nullable=False
    )
    file_path = Column(String, nullable=False, unique=True, index=True)
    upload_date = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
