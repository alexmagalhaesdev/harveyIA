from pydantic import BaseModel


class ChatMessageSchema(BaseModel):
    user_prompt: str
