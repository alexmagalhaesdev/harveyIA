from enum import Enum
from pydantic import BaseModel


class IntegrationType(str, Enum):
    WHATSAPP: str = "WhatsApp"
    GMAIL: str = "Gmail"


class IntegrationSchema(BaseModel):
    integration_name: str
    integration_type: IntegrationType
