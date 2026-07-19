from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.disk import Disk


class DiskRepository:

    def __init__(self, db: Session):
        self.db = db

    # CREATE SINGLE
    def create(self, device_id: int, disk) -> Disk:

        db_disk = Disk(
            device_id=device_id,
            device_name=disk.device_name,
            filesystem=disk.filesystem,
            mount_point=disk.mount_point,
            total_bytes=disk.total_bytes,
            used_bytes=disk.used_bytes,
            free_bytes=disk.free_bytes,
        )

        self.db.add(db_disk)
        return db_disk

    # CREATE MULTIPLE
    def create_many(self, device_id: int, disks) -> list[Disk]:

        created_disks = []

        for disk in disks:
            created_disks.append(self.create(device_id, disk))

        return created_disks

    # GET BY DISK ID
    def get_by_id(self, disk_id: int) -> Disk | None:

        return self.db.get(Disk, disk_id)

    # GET ALL DISKS OF A Device
    def get_by_device_id(self, device_id: int) -> list[Disk]:

        stmt = (
            select(Disk).where(Disk.device_id == device_id).order_by(Disk.mount_point)
        )

        return self.db.scalars(stmt).all()

    # GET ALL DISKS
    def get_all(self) -> list[Disk]:

        stmt = select(Disk).order_by(Disk.device_id, Disk.mount_point)

        return self.db.scalars(stmt).all()

    # DELETE ALL DISKS OF A DEVICE
    def delete_by_device(self, device_id: int) -> None:

        self.db.query(Disk).filter(Disk.device_id == device_id).delete(
            synchronize_session=False
        )
