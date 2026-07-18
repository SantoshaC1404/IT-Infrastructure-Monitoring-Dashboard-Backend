from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.constants import API_TAG_HEALTH
from app.api.deps import get_db

router = APIRouter(tags=[API_TAG_HEALTH])


@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Health check endpoint to verify the application's health status.
    Args:
        db (Session): SQLAlchemy database session provided by the get_db dependency.
    Returns:
        dict: A dictionary containing the health status, application name, and version.
    """
    try:
        # Perform a simple database query to verify connectivity
        db.execute(text("SELECT 1"))
        database = "Connected"

    except Exception as e:
        database = "Disconnected"

    return {
        "status": "healthy",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database": database,
    }
