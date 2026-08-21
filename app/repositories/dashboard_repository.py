from sqlalchemy import and_, case, func, or_, select
from sqlalchemy.orm import Session

from app.dto.dashboard.critical_device_dto import CriticalDevicesDTO
from app.dto.dashboard.dashboard_device_dto import DashboardDeviceDTO
from app.dto.dashboard.dashboard_summary_dto import DashboardSummaryDTO
from app.models.device import Device
from app.models.monitoring_snapshot import MonitoringSnapshot
from app.utils.enums import DeviceStatus, DeviceType
from app.utils.constants import (
    CPU_THRESHOLD,
    MEMORY_THRESHOLD,
    DISK_THRESHOLD,
)


class DashboardRepository:

    # CPU_THRESHOLD = 90
    # MEMORY_THRESHOLD = 90
    # DISK_THRESHOLD = 90

    def __init__(self, db: Session):
        self.db = db

    def _latest_snapshot_subquery(self):
        """
        Latest monitoring snapshot for each device.
        """

        return (
            select(
                MonitoringSnapshot.device_id,
                func.max(MonitoringSnapshot.collected_at).label("latest"),
            )
            .group_by(MonitoringSnapshot.device_id)
            .subquery()
        )

    # ------------------------------------------------------------------
    # Dashboard Summary
    # ------------------------------------------------------------------

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
                            [
                                DeviceType.LINUX,
                                DeviceType.WINDOWS,
                            ]
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

    # ------------------------------------------------------------------
    # Dashboard Devices
    # ------------------------------------------------------------------

    def get_dashboard_devices(self):

        latest = self._latest_snapshot_subquery()

        stmt = (
            select(
                Device.id,
                Device.name,
                Device.ip_address,
                Device.status,
                Device.monitoring_enabled,
                MonitoringSnapshot.cpu_usage,
                MonitoringSnapshot.memory_usage,
                MonitoringSnapshot.disk_usage,
            )
            .outerjoin(
                latest,
                latest.c.device_id == Device.id,
            )
            .outerjoin(
                MonitoringSnapshot,
                and_(
                    MonitoringSnapshot.device_id == latest.c.device_id,
                    MonitoringSnapshot.collected_at == latest.c.latest,
                ),
            )
            .order_by(Device.name)
        )

        rows = self.db.execute(stmt).all()

        return [
            DashboardDeviceDTO(
                id=row.id,
                name=row.name,
                ip_address=row.ip_address,
                status=row.status.name,
                monitoring_enabled=row.monitoring_enabled,
                cpu_usage=row.cpu_usage or 0,
                memory_usage=row.memory_usage or 0,
                disk_usage=row.disk_usage or 0,
            )
            for row in rows
        ]

    # ------------------------------------------------------------------
    # Critical Devices
    # ------------------------------------------------------------------

    def get_critical_devices(self):

        latest = self._latest_snapshot_subquery()

        stmt = (
            select(
                Device.id,
                Device.name,
                Device.ip_address,
                Device.status,
                MonitoringSnapshot.cpu_usage,
                MonitoringSnapshot.memory_usage,
                MonitoringSnapshot.disk_usage,
            )
            .outerjoin(
                latest,
                latest.c.device_id == Device.id,
            )
            .outerjoin(
                MonitoringSnapshot,
                and_(
                    MonitoringSnapshot.device_id == latest.c.device_id,
                    MonitoringSnapshot.collected_at == latest.c.latest,
                ),
            )
            .where(
                or_(
                    Device.status == DeviceStatus.OFFLINE,
                    MonitoringSnapshot.cpu_usage >= CPU_THRESHOLD,
                    MonitoringSnapshot.memory_usage >= MEMORY_THRESHOLD,
                    MonitoringSnapshot.disk_usage >= DISK_THRESHOLD,
                )
            )
            .order_by(Device.name)
        )

        rows = self.db.execute(stmt).all()

        devices = []

        for row in rows:

            if row.status == DeviceStatus.OFFLINE:
                reason = "Device Offline"

            elif (row.cpu_usage or 0) >= CPU_THRESHOLD:
                reason = "High CPU"

            elif (row.memory_usage or 0) >= MEMORY_THRESHOLD:
                reason = "High Memory"

            elif (row.disk_usage or 0) >= DISK_THRESHOLD:
                reason = "High Disk"

            else:
                reason = "Critical"

            devices.append(
                CriticalDevicesDTO(
                    id=row.id,
                    name=row.name,
                    ip_address=row.ip_address,
                    status=row.status.name,
                    cpu_usage=row.cpu_usage or 0,
                    memory_usage=row.memory_usage or 0,
                    disk_usage=row.disk_usage or 0,
                    critical_reason=reason,
                )
            )

        return devices
