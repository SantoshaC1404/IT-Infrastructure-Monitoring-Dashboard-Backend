from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.disk import Disk


class DiskRepository:

    def __init__(self, db: Session):
        self.db = db

    # CREATE SINGLE
    def create(self, server_id: int, disk) -> Disk:

        db_disk = Disk(
            server_id=server_id,
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
    def create_many(self, server_id: int, disks) -> list[Disk]:

        created_disks = []

        for disk in disks:
            created_disks.append(self.create(server_id, disk))

        return created_disks

    # GET BY DISK ID
    def get_by_id(self, disk_id: int) -> Disk | None:

        return self.db.get(Disk, disk_id)

    # GET ALL DISKS OF A SERVER
    def get_by_server_id(self, server_id: int) -> list[Disk]:

        stmt = (
            select(Disk).where(Disk.server_id == server_id).order_by(Disk.mount_point)
        )

        return self.db.scalars(stmt).all()

    # GET ALL DISKS
    def get_all(self) -> list[Disk]:

        stmt = select(Disk).order_by(Disk.server_id, Disk.mount_point)

        return self.db.scalars(stmt).all()

    # DELETE ALL DISKS OF A SERVER
    def delete_by_server(self, server_id: int) -> None:

        self.db.query(Disk).filter(Disk.server_id == server_id).delete(
            synchronize_session=False
        )
