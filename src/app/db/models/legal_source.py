from db.base_class import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.sql import func


class LegalSource(Base):
    id = Column(Integer, primary_key=True, index=True)
    source_name = Column(String, nullable=False, index=True)
    source_url = Column(String, nullable=True)
    source_type = Column(
        ENUM("Jurisprudência", "Lei", name="source_type_enum"),
        nullable=False,
        index=True,
    )
    created_at = Column(DateTime, default=func.now(), nullable=False)
