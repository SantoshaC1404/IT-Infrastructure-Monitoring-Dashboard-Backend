from sqlalchemy.orm import Session

from app.services.dashboard.critical_devices_service import CriticalDevicesService
from app.services.dashboard.dashboard_devices_service import DashboardDevicesService
from app.services.dashboard.dashboard_summary_service import DashboardSummaryService


class DashboardService:

    def __init__(self, db: Session):

        self.summary_service = DashboardSummaryService(db)

        self.devices_service = DashboardDevicesService(db)

        self.critical_service = CriticalDevicesService(db)

    # Get dashboard summary
    def get_dasgboard_summary(self):

        return self.summary_service.get_summary()

    # Get dashboard devices with latest monitoring snapshot
    def get_dashboard_devices(self):

        return self.devices_service.get_devices()

    # Get Critical Devices
    def get_critical_devices(self):

        return self.critical_service.get_critical_devices()
