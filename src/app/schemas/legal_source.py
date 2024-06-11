from enum import Enum
from pydantic import BaseModel, HttpUrl


class LegalSourceType(str, Enum):
    LEI: str = "Lei"
    JURISPRUDENCIA: str = "Jurisprudência"


class LegalSourceSchema(BaseModel):
    source_name: str
    source_url: HttpUrl
    source_type: LegalSourceType
