from sqlalchemy import and_, func, or_, select
from sqlalchemy.orm import Session, joinedload
import re

from app.models.device import Device
from app.models.monitoring_snapshot import MonitoringSnapshot
from app.repositories.base_repository import BaseRepository

from app.utils.constants import (
    CPU_THRESHOLD,
    DISK_THRESHOLD,
    MEMORY_THRESHOLD,
)


class DeviceRepository(BaseRepository[Device]):

    def __init__(self, db: Session):
        super().__init__(db)

    # ---------------------------------------------------------
    # HELPER: APPLY MONITORING DATA
    # ---------------------------------------------------------

    def _apply_monitoring_data(self, device, row):
        device.cpu_usage = row[1] or 0.0
        device.memory_usage = row[2] or 0.0
        device.disk_usage = row[3] or 0.0

        device.uptime = row[4]

        raw_login = row[5]

        if raw_login:
            match = re.search(
                r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b",
                raw_login,
            )

            device.login_source = match.group(0) if match else device.ip_address
        else:
            device.login_source = None

        device.last_login_time = row[6]

        return device

    # ---------------------------------------------------------
    # HELPER: CALCULATE CRITICAL REASONS
    # ---------------------------------------------------------

    def _get_critical_reasons(self, device):

        reasons = []

        if device.cpu_usage is not None:
            if device.cpu_usage >= CPU_THRESHOLD:
                reasons.append("CPU High")

        if device.memory_usage is not None:
            if device.memory_usage >= MEMORY_THRESHOLD:
                reasons.append("Memory High")

        if device.disk_usage is not None:
            if device.disk_usage >= DISK_THRESHOLD:
                reasons.append("Disk High")

        return reasons

    # ---------------------------------------------------------
    # GET ALL
    # ---------------------------------------------------------

    def get_all(self):

        latest_snapshot = (
            select(
                MonitoringSnapshot.device_id,
                func.max(MonitoringSnapshot.collected_at).label("latest"),
            )
            .group_by(MonitoringSnapshot.device_id)
            .subquery()
        )

        stmt = (
            select(
                Device,
                MonitoringSnapshot.cpu_usage,
                MonitoringSnapshot.memory_usage,
                MonitoringSnapshot.disk_usage,
                MonitoringSnapshot.uptime,
                MonitoringSnapshot.login_source,
                MonitoringSnapshot.last_login_time,
            )
            .outerjoin(
                latest_snapshot,
                latest_snapshot.c.device_id == Device.id,
            )
            .outerjoin(
                MonitoringSnapshot,
                and_(
                    MonitoringSnapshot.device_id == latest_snapshot.c.device_id,
                    MonitoringSnapshot.collected_at == latest_snapshot.c.latest,
                ),
            )
            .options(joinedload(Device.inventory))
            .order_by(Device.name)
        )

        rows = self.db.execute(stmt).all()

        devices = []

        for row in rows:

            device = self._apply_monitoring_data(
                row[0],
                row,
            )

            device.critical_reasons = self._get_critical_reasons(device)

            devices.append(device)

        return devices

    # ---------------------------------------------------------
    # GET BY ID
    # ---------------------------------------------------------

    def get_by_id(self, device_id: int):

        latest_snapshot = (
            select(
                MonitoringSnapshot.device_id,
                func.max(MonitoringSnapshot.collected_at).label("latest"),
            )
            .group_by(MonitoringSnapshot.device_id)
            .subquery()
        )

        stmt = (
            select(
                Device,
                MonitoringSnapshot.cpu_usage,
                MonitoringSnapshot.memory_usage,
                MonitoringSnapshot.disk_usage,
                MonitoringSnapshot.uptime,
                MonitoringSnapshot.login_source,
                MonitoringSnapshot.last_login_time,
            )
            .outerjoin(
                latest_snapshot,
                latest_snapshot.c.device_id == Device.id,
            )
            .outerjoin(
                MonitoringSnapshot,
                and_(
                    MonitoringSnapshot.device_id == latest_snapshot.c.device_id,
                    MonitoringSnapshot.collected_at == latest_snapshot.c.latest,
                ),
            )
            .options(joinedload(Device.inventory))
            .where(Device.id == device_id)
        )

        row = self.db.execute(stmt).first()

        if row is None:
            return None

        device = self._apply_monitoring_data(
            row[0],
            row,
        )

        device.critical_reasons = self._get_critical_reasons(device)

        return device

    # ---------------------------------------------------------
    # GET BY IP
    # ---------------------------------------------------------

    def get_by_ip(self, ip_address: str):

        latest_snapshot = (
            select(
                MonitoringSnapshot.device_id,
                func.max(MonitoringSnapshot.collected_at).label("latest"),
            )
            .group_by(MonitoringSnapshot.device_id)
            .subquery()
        )

        stmt = (
            select(
                Device,
                MonitoringSnapshot.cpu_usage,
                MonitoringSnapshot.memory_usage,
                MonitoringSnapshot.disk_usage,
                MonitoringSnapshot.uptime,
                MonitoringSnapshot.login_source,
                MonitoringSnapshot.last_login_time,
            )
            .outerjoin(
                latest_snapshot,
                latest_snapshot.c.device_id == Device.id,
            )
            .outerjoin(
                MonitoringSnapshot,
                and_(
                    MonitoringSnapshot.device_id == latest_snapshot.c.device_id,
                    MonitoringSnapshot.collected_at == latest_snapshot.c.latest,
                ),
            )
            .where(Device.ip_address == ip_address)
        )

        row = self.db.execute(stmt).first()

        if row is None:
            return None

        device = self._apply_monitoring_data(
            row[0],
            row,
        )

        device.critical_reasons = self._get_critical_reasons(device)

        return device

    # ---------------------------------------------------------
    # CREATE
    # ---------------------------------------------------------

    def create(
        self,
        device: Device,
        commit: bool = True,
    ):

        self.db.add(device)

        if commit:
            self.db.commit()
            self.db.refresh(device)

        return device

    # ---------------------------------------------------------
    # UPDATE
    # ---------------------------------------------------------

    def update(self, device: Device):

        self.db.flush()

        return device

    # ---------------------------------------------------------
    # DELETE
    # ---------------------------------------------------------

    def delete(
        self,
        device: Device,
        commit: bool = True,
    ):

        self.db.delete(device)

        if commit:
            self.db.commit()

    # ---------------------------------------------------------
    # GET MONITORING ENABLED
    # ---------------------------------------------------------

    def get_monitoring_enabled(self):

        stmt = select(Device).where(Device.monitoring_enabled.is_(True))

        return list(self.db.scalars(stmt).all())

    # ---------------------------------------------------------
    # GET CRITICAL DEVICES
    # ---------------------------------------------------------

    def critical_devices(self):

        latest_snapshot = (
            select(
                MonitoringSnapshot.device_id,
                func.max(MonitoringSnapshot.collected_at).label("latest"),
            )
            .group_by(MonitoringSnapshot.device_id)
            .subquery()
        )

        stmt = (
            select(
                Device,
                MonitoringSnapshot.cpu_usage,
                MonitoringSnapshot.memory_usage,
                MonitoringSnapshot.disk_usage,
                MonitoringSnapshot.uptime,
                MonitoringSnapshot.login_source,
                MonitoringSnapshot.last_login_time,
            )
            .join(
                latest_snapshot,
                latest_snapshot.c.device_id == Device.id,
            )
            .join(
                MonitoringSnapshot,
                and_(
                    MonitoringSnapshot.device_id == latest_snapshot.c.device_id,
                    MonitoringSnapshot.collected_at == latest_snapshot.c.latest,
                ),
            )
            .options(joinedload(Device.inventory))
            .where(
                or_(
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

            device = self._apply_monitoring_data(
                row[0],
                row,
            )

            device.critical_reasons = self._get_critical_reasons(device)

            devices.append(device)

        return devices
