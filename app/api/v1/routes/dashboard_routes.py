from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.dashboard.dashboard_devices import DashboardDevicesResponse
from app.services.dashboard.dashboard_service import DashboardService
from app.schemas.dashboard.dashboard import DashboardSummaryResponse

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/summary",
    response_model=DashboardSummaryResponse,
)
def get_dashboard_summary(
    db: Session = Depends(get_db),
):

    return DashboardService(db).get_dasgboard_summary()


@router.get(
    "/devices",
    response_model=DashboardDevicesResponse,
)
def get_dashboard_devices(
    db: Session = Depends(get_db),
):

    return DashboardService(db).get_dashboard_devices()