from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services.dashboard_service import DashboardService

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/summary")
def summary(
    db: Session = Depends(get_db),
):

    return DashboardService(db).summary()
