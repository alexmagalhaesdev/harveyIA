from datetime import datetime
from pydantic import BaseModel
from enum import Enum


class DocumentType(str, Enum):
    PDF: str = "PDF"
    DOCX: str = "DOCX"


class DocumentSchema(BaseModel):
    document_name: str
    document_type: DocumentType
    upload_date: datetime
