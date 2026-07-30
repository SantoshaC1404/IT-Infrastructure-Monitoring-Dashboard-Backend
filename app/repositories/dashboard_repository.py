from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.models.device import Device
from app.utils.enums import DeviceStatus, DeviceType
from app.dto.dashboard_summary_dto import DashboardSummaryDTO


class DashboardRepository:

    def __init__(self, db: Session):

        self.db = db

    def get_summary(self):

        summary = self.db.query(
            func.count(Device.id).label("total_devices"),
            func.sum(
                case(
                    (Device.status == DeviceStatus.ONLINE, 1),
                    else_=0,
                )
            ).label("online_devices"),
            func.sum(
                case(
                    (Device.status == DeviceStatus.OFFLINE, 1),
                    else_=0,
                )
            ).label("offline_devices"),
            func.sum(
                case(
                    (Device.monitoring_enabled.is_(True), 1),
                    else_=0,
                )
            ).label("monitoring_enabled"),
            func.sum(
                case(
                    (Device.monitoring_enabled.is_(False), 1),
                    else_=0,
                )
            ).label("monitoring_disabled"),
            func.sum(
                case(
                    (Device.device_type == DeviceType.LINUX, 1),
                    else_=0,
                )
            ).label("linux_devices"),
            func.sum(
                case(
                    (Device.device_type == DeviceType.WINDOWS, 1),
                    else_=0,
                )
            ).label("windows_devices"),
            func.sum(
                case(
                    (
                        Device.device_type.notin_(
                            [DeviceType.LINUX, DeviceType.WINDOWS]
                        ),
                        1,
                    ),
                    else_=0,
                )
            ).label("network_devices"),
        ).one()

        return DashboardSummaryDTO(
            total_devices=summary.total_devices or 0,
            online_devices=summary.online_devices or 0,
            offline_devices=summary.offline_devices or 0,
            monitoring_enabled=summary.monitoring_enabled or 0,
            monitoring_disabled=summary.monitoring_disabled or 0,
            device_types={
                "LINUX": summary.linux_devices or 0,
                "WINDOWS": summary.windows_devices or 0,
                "NETWORK": summary.network_devices or 0,
            },
        )

    """
    def average_cpu(self):

        stmt = select(func.avg(MonitoringSnapshot.cpu_usage))

        return self.db.scalar(stmt)
    """

    """
    def average_memory(self):

        stmt = select(func.avg(MonitoringSnapshot.memory_usage))

        return self.db.scalar(stmt)
    """

    """
    def average_disk(self):

        stmt = select(func.avg(MonitoringSnapshot.disk_usage))

        return self.db.scalar(stmt)
    """
