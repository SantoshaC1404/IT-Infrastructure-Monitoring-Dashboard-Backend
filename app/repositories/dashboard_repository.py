from sqlalchemy import func, select

from app.models.device import Devices
from app.models.monitoring_snapshot import MonitoringSnapshot
from app.utils.enums import DeviceStatus


class DashboardRepository:

    def __init__(self, db):
        self.db = db

    def total_devices(self):

        stmt = select(func.count(Devices.id))

        return self.db.scalar(stmt)

    def online_devices(self):

        stmt = select(func.count(Devices.id)).where(
            Devices.status == DeviceStatus.ONLINE
        )

        return self.db.scalar(stmt)

    def offline_devices(self):

        stmt = select(func.count(Devices.id)).where(
            Devices.status == DeviceStatus.OFFLINE
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
