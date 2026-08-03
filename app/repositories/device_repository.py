from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session, joinedload
import re

from app.models.device import Device
from app.models.monitoring_snapshot import MonitoringSnapshot
from app.repositories.base_repository import BaseRepository


class DeviceRepository(BaseRepository[Device]):

    def __init__(self, db: Session):
        super().__init__(db)

    # GET ALL
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
            device = row[0]
            device.cpu_usage = row[1] or 0.0
            device.memory_usage = row[2] or 0.0
            device.disk_usage = row[3] or 0.0
            raw_login = row[4]
            if raw_login:
                m = re.search(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", raw_login)
                device.login_source = m.group(0) if m else device.ip_address
            else:
                device.login_source = None
            device.last_login_time = row[5]
            devices.append(device)

        return devices

    # GET BY ID
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
                MonitoringSnapshot.login_source,
                MonitoringSnapshot.last_login_time,
            )
            .outerjoin(latest_snapshot, latest_snapshot.c.device_id == Device.id)
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

        device = row[0]
        device.cpu_usage = row[1] or 0.0
        device.memory_usage = row[2] or 0.0
        device.disk_usage = row[3] or 0.0
        raw_login = row[4]
        if raw_login:
            m = re.search(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", raw_login)
            device.login_source = m.group(0) if m else device.ip_address
        else:
            device.login_source = None
        device.last_login_time = row[5]
        return device

    # GET BY IP
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
                MonitoringSnapshot.login_source,
                MonitoringSnapshot.last_login_time,
            )
            .outerjoin(latest_snapshot, latest_snapshot.c.device_id == Device.id)
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

        device = row[0]
        device.cpu_usage = row[1] or 0.0
        device.memory_usage = row[2] or 0.0
        device.disk_usage = row[3] or 0.0
        raw_login = row[4]
        if raw_login:
            m = re.search(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", raw_login)
            device.login_source = m.group(0) if m else device.ip_address
        else:
            device.login_source = None
        device.last_login_time = row[5]
        return device

    # CREATE
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

    # UPDATE
    def update(self, device: Device):
        self.db.flush()
        return device

    # DELETE
    def delete(
        self,
        device: Device,
        commit: bool = True,
    ):
        self.db.delete(device)
        if commit:
            self.db.commit()

    # GET MONITORING STATUS
    def get_monitoring_enabled(self):

        stmt = select(Device).where(Device.monitoring_enabled.is_(True))

        return list(self.db.scalars(stmt).all())
