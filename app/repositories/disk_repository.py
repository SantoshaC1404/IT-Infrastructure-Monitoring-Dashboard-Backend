from sqlalchemy.orm import Session

from app.models.disk import Disk


class DiskRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, server_id: int, disk):

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

    def create_many(self, server_id: int, disks):

        created = []

        for disk in disks:
            created.append(self.create(server_id, disk))

        return created

    def delete_by_server(self, server_id: int):

        self.db.query(Disk).filter(Disk.server_id == server_id).delete()
