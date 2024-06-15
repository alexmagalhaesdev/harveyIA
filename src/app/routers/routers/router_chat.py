from fastapi import APIRouter, Request, status
from core.ui_config import templates

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
def get_chat(request: Request):
    return templates.TemplateResponse("pages/chat.html", {"request": request})
