from openai import OpenAI
from core.config import settings

openai_client = OpenAI(api_key=settings.openai.OPENAI_API_KEY)
