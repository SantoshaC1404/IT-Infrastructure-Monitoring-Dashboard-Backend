from app.repositories.dashboard_repository import DashboardRepository


class DashboardService:

    def __init__(self, db):

        self.repo = DashboardRepository(db)

    def summary(self):

        return {
            "total_devices": self.repo.total_devices(),
            "online_devices": self.repo.online_devices(),
            "offline_devices": self.repo.offline_devices(),
            "average_cpu": self.repo.average_cpu(),
            "average_memory": self.repo.average_memory(),
            "average_disk": self.repo.average_disk(),
        }
