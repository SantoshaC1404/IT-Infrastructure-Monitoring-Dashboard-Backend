from sqlalchemy import func, select

from app.models.server import Server
from app.models.monitoring_snapshot import MonitoringSnapshot
from app.utils.enums import ServerStatus


class DashboardRepository:

    def __init__(self, db):
        self.db = db

    def total_servers(self):

        stmt = select(func.count(Server.id))

        return self.db.scalar(stmt)

    def online_servers(self):

        stmt = select(func.count(Server.id)).where(Server.status == ServerStatus.ONLINE)

        return self.db.scalar(stmt)

    def offline_servers(self):

        stmt = select(func.count(Server.id)).where(
            Server.status == ServerStatus.OFFLINE
        )

        return self.db.scalar(stmt)

    def average_cpu(self):

        stmt = select(func.avg(MonitoringSnapshot.cpu_usage))

        return self.db.scalar(stmt)

    def average_memory(self):

        stmt = select(func.avg(MonitoringSnapshot.memory_usage))

        return self.db.scalar(stmt)

    def average_disk(self):

        stmt = select(func.avg(MonitoringSnapshot.disk_usage))

        return self.db.scalar(stmt)
