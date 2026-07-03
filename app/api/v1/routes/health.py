from fastapi import APIRouter

from app.core.config import settings
from app.core.constants import API_TAG_HEALTH

router = APIRouter(tags=[API_TAG_HEALTH])


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }
