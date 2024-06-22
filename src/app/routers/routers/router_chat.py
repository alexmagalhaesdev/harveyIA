from fastapi import APIRouter, Request, status

from schemas.chat_message import ChatMessageSchema
from orchestrator.orchestrator import PromptOrchestrator
from core.ui_config import templates

router = APIRouter()

# instance prompt orchestrator class
rag = PromptOrchestrator()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
)
def get_chat(request: Request):
    return templates.TemplateResponse("pages/chat.html", {"request": request})


@router.post("/", status_code=status.HTTP_200_OK)
def post_chat(user_prompt: ChatMessageSchema):
    response = rag.answer_query(query=user_prompt.user_prompt)
    return response
