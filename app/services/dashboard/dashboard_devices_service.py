from sqlalchemy.orm import Session

from app.repositories.dashboard_repository import DashboardRepository
from app.schemas.dashboard.dashboard_devices import (
    DashboardDeviceResponse,
    DashboardDevicesResponse,
)


class DashboardDevicesService:

    def __init__(self, db: Session):

        self.repository = DashboardRepository(db)

    def get_devices(self) -> DashboardDevicesResponse:

        devices = self.repository.get_dashboard_devices()

        return DashboardDevicesResponse(
            devices=[
                DashboardDeviceResponse(
                    id=device.id,
                    name=device.name,
                    ip_address=device.ip_address,
                    status=device.status,
                    monitoring_enabled=device.monitoring_enabled,
                    cpu_usage=device.cpu_usage,
                    memory_usage=device.memory_usage,
                    disk_usage=device.disk_usage,
                )
                for device in devices
            ]
        )
