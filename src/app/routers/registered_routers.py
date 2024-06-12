from fastapi import APIRouter
from routers.routers import (
    router_auth,
    router_chat,
    router_documents,
    router_templates,
    router_legal_source,
    router_integrations,
    router_pricing,
    router_settings,
)


router = APIRouter()

router.include_router(router_auth.router, prefix="/auth", tags=["auth"])
router.include_router(router_chat.router, prefix="/chat", tags=["chat"])
router.include_router(router_documents.router, prefix="/documents", tags=["documents"])
router.include_router(router_templates.router, prefix="/templates", tags=["templates"])
router.include_router(
    router_legal_source.router, prefix="/legal_source", tags=["legal_source"]
)
router.include_router(
    router_integrations.router, prefix="/integrations", tags=["integrations"]
)
router.include_router(router_pricing.router, prefix="/pricing", tags=["pricing"])
router.include_router(router_settings.router, prefix="/settings", tags=["settings"])
