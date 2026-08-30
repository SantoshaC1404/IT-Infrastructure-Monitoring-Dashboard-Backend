from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.dashboard.critical_devices_schema import (
    CriticalDeviceResponse,
    CriticalDevicesResponse,
)
from app.schemas.dashboard.dashboard import DashboardSummaryResponse
from app.schemas.dashboard.dashboard_devices import DashboardDevicesResponse
from app.services.dashboard.dashboard_service import DashboardService

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


@router.get(
    "/critical-devices",
    response_model=CriticalDevicesResponse,
)
def get_critical_devices(
    db: Session = Depends(get_db),
):

    devices = DashboardService(db).get_critical_devices()

    return CriticalDevicesResponse(
        critical_devices=[
            CriticalDeviceResponse(
                id=device.id,
                name=device.name,
                ip_address=device.ip_address,
                status=device.status,
                cpu_usage=device.cpu_usage,
                memory_usage=device.memory_usage,
                disk_usage=device.disk_usage,
                critical_reason=device.critical_reason,
            )
            for device in devices
        ]
    )
