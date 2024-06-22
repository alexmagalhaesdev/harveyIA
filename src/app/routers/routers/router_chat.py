from fastapi import APIRouter, Request, status


# from fastapi.responses import HTMLResponse
# from core.security.auth_bearer import JWTBearer
from schemas.chat_message import ChatMessageSchema

from orchestrator.main_orchestrator import query_engine

from core.ui_config import templates

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
)
def get_chat(request: Request):
    return templates.TemplateResponse("pages/chat.html", {"request": request})


@router.post("/", status_code=status.HTTP_200_OK)
def post_chat(user_prompt: ChatMessageSchema):
    response = query_engine.query(user_prompt.user_prompt)
    return response
