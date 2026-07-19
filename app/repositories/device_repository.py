from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.device import Device
from app.repositories.base_repository import BaseRepository


class DeviceRepository(BaseRepository[Device]):

    def __init__(self, db: Session):
        super().__init__(db)

    # GET ALL
    def get_all(self):
        stmt = (
            select(Device).options(joinedload(Device.inventory)).order_by(Device.name)
        )

        return list(self.db.scalars(stmt).unique())

    # GET BY ID
    def get_by_id(self, device_id: int):
        stmt = (
            select(Device)
            .options(joinedload(Device.inventory))
            .where(Device.id == device_id)
        )

        return self.db.scalar(stmt)

    # GET BY IP
    def get_by_ip(self, ip_address: str):

        stmt = select(Device).where(Device.ip_address == ip_address)

        return self.db.scalar(stmt)

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
