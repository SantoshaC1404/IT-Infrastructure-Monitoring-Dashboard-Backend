from sqlalchemy.orm import Session

from app.repositories.dashboard_repository import DashboardRepository


class CriticalDevicesService:

    def __init__(self, db: Session):
        self.repository = DashboardRepository(db)

    def get_critical_devices(self):

        return self.repository.get_critical_devices()
