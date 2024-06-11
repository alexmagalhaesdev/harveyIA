from enum import Enum
from pydantic import BaseModel


class TemplateType(str, Enum):
    PETICAO: str = "Petição"
    APELACAO: str = "Apelação"
    CONTESTACAO: str = "Contestação"


class TemplateSchema(BaseModel):
    template_name: str
    template_content: str
    template_type: TemplateType
