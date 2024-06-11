from fastapi import APIRouter
from routers.routers import router_auth

router = APIRouter()

router.include_router(router_auth.router, prefix="/auth", tags=["auth"])
