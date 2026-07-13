from app.repositories.dashboard_repository import DashboardRepository


class DashboardService:

    def __init__(self, db):

        self.repo = DashboardRepository(db)

    def summary(self):

        return {
            "total_servers": self.repo.total_servers(),
            "online_servers": self.repo.online_servers(),
            "offline_servers": self.repo.offline_servers(),
            "average_cpu": self.repo.average_cpu(),
            "average_memory": self.repo.average_memory(),
            "average_disk": self.repo.average_disk(),
        }
